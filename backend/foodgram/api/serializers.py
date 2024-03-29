from django.db.transaction import atomic
from django.shortcuts import get_object_or_404
from djoser.serializers import UserSerializer
from drf_base64.fields import Base64ImageField
from recipes.models import (Favourite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)
from rest_framework.serializers import (IntegerField, ModelSerializer,
                                        PrimaryKeyRelatedField,
                                        SerializerMethodField,
                                        SlugRelatedField, ValidationError)
from users.models import Subscription, User


class CustomUserSerializer(UserSerializer):
    """ Сериализатор пользователя. """

    is_subscribed = SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        ]

    def get_is_subscribed(self, obj: User):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Subscription.objects.filter(
            user=request.user, author=obj).exists()


class TagSerializer(ModelSerializer):
    """ Сериализатор просмотра Тегов. """

    class Meta:
        model = Tag
        fields = [
            'id',
            'name',
            'color',
            'slug'
        ]


class IngredientSerializer(ModelSerializer):
    """ Сериализатор просмотра Ингредиентов. """

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit'
        )


class RecipeShortSerializer(ModelSerializer):

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class SubscriptionsSerializer(ModelSerializer):
    """ Сериализатор просмотра Подписок. """

    recipes_count = SerializerMethodField()
    recipes = SerializerMethodField()
    is_subscribed = SerializerMethodField(read_only=True)

    class Meta(CustomUserSerializer.Meta):
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count'
        )

    def get_recipes_count(self, author):
        return Recipe.objects.filter(author=author).count()

    def get_recipes(self, author):
        queryset = self.context.get('request')
        recipes_limit = queryset.query_params.get('recipes_limit')
        if recipes_limit:
            return RecipeShortSerializer(
                Recipe.objects.filter(author=author)[:int(recipes_limit)],
                many=True, context={'request': queryset}
            ).data
        return RecipeShortSerializer(
            Recipe.objects.filter(author=author),
            many=True,
            context={'request': queryset}
        ).data

    def get_is_subscribed(self, author):
        return Subscription.objects.filter(
            user=self.context.get('request').user,
            author=author
        ).exists()


class SubscribeSerializer(ModelSerializer):
    """ Сериализатор функции Подписки. """

    class Meta:
        model = Subscription
        fields = ('user', 'author')

    def validate(self, data):
        get_object_or_404(User, username=data['author'])
        if self.context['request'].user == data['author']:
            raise ValidationError({
                'errors': 'Нельзя подписаться на себя.'
            })
        if Subscription.objects.filter(
                user=self.context['request'].user,
                author=data['author']
        ):
            raise ValidationError({
                'errors': 'Уже подписан.'
            })
        return data

    def to_representation(self, instance):
        return SubscriptionsSerializer(
            instance.author,
            context={'request': self.context.get('request')}
        ).data


class RecipeIngredientsSerializer(ModelSerializer):
    """ Сериализатор просмотра ингредиента в рецепте. """

    id = PrimaryKeyRelatedField(
        source='ingredient',
        read_only=True
    )
    measurement_unit = SlugRelatedField(
        source='ingredient',
        slug_field='measurement_unit',
        read_only=True,
    )
    name = SlugRelatedField(
        source='ingredient',
        slug_field='name',
        read_only=True,
    )

    class Meta:
        model = RecipeIngredient
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )


class RecipeSerializer(ModelSerializer):
    """ Сериализатор просмотра Рецепта. """

    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = RecipeIngredientsSerializer(
        many=True,
        read_only=True,
        source='ingridients_recipe',
    )
    is_favorited = SerializerMethodField(read_only=True)
    is_in_shopping_cart = SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = [
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        ]

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return Favourite.objects.filter(
            user=request.user, recipe__id=obj.id
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(
            user=request.user, recipe__id=obj.id
        ).exists()


class CreateIngredientRecipeSerializer(ModelSerializer):
    """ Сериализатор добавления ингредиента в рецепт. """

    id = PrimaryKeyRelatedField(
        source='ingredient',
        queryset=Ingredient.objects.all()
    )

    class Meta:
        model = RecipeIngredient
        fields = (
            'id',
            'amount',
        )

    def validate_amount(self, data):
        if int(data) < 1:
            raise ValidationError({
                'ingredients': (
                    'Количество должно быть больше 1'
                ),
                'msg': data
            })
        return data

    def create(self, validated_data):
        return RecipeIngredient.objects.create(
            ingredient=validated_data.get('id'),
            amount=validated_data.get('amount')
        )


class RecipeCreateSerializer(ModelSerializer):
    """ Сериализатор создания/обновления рецепта. """

    image = Base64ImageField(use_url=True, max_length=None)
    author = CustomUserSerializer(read_only=True)
    ingredients = CreateIngredientRecipeSerializer(many=True)
    tags = PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    image = Base64ImageField()
    cooking_time = IntegerField()

    class Meta:
        model = Recipe
        fields = [
            'id',
            'author',
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time'
        ]

    def create_ingredients(self, recipe, ingredients):
        RecipeIngredient.objects.bulk_create([
            RecipeIngredient(
                recipe=recipe,
                amount=ingredient['amount'],
                ingredient=ingredient['ingredient'],
            ) for ingredient in ingredients
        ])

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        ingredients_list = []
        for ingredient in ingredients:
            ingredient_id = ingredient['id']
            if ingredient_id in ingredients_list:
                raise ValidationError(
                    'Есть задублированные ингредиенты!'
                )
            ingredients_list.append(ingredient_id)
        if data['cooking_time'] <= 0:
            raise ValidationError(
                'Время приготовления должно быть больше 0!'
            )
        return data

    @atomic
    def create(self, validated_data):
        request = self.context.get('request')
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(
            author=request.user,
            **validated_data
        )
        self.create_ingredients(recipe, ingredients)
        recipe.tags.set(tags)
        return recipe

    @atomic
    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        recipe = instance
        RecipeIngredient.objects.filter(recipe=recipe).delete()
        self.create_ingredients(recipe, ingredients)
        return super().update(recipe, validated_data)

    def to_representation(self, instance):
        return RecipeSerializer(
            instance,
            context={
                'request': self.context.get('request'),
            }
        ).data


class ShoppingCartSerializer(ModelSerializer):
    """ Сериализатор для списка покупок. """

    class Meta:
        fields = ['recipe', 'user']
        model = ShoppingCart

    def validate(self, data):
        request = self.context.get('request')
        recipe = data['recipe']
        if ShoppingCart.objects.filter(
            user=request.user, recipe=recipe
        ).exists():
            raise ValidationError({
                'errors': 'Данный рецепт уже есть в корзине.'
            })
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeShortSerializer(instance.recipe, context=context).data


class FavoriteSerializer(ModelSerializer):
    """ Сериализатор для отображения избранного. """

    class Meta:
        model = Favourite
        fields = ('user', 'recipe')

    def validate(self, data):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        recipe = data['recipe']
        if Favourite.objects.filter(user=request.user, recipe=recipe).exists():
            raise ValidationError({
                'errors': 'Уже есть в избранном.'
            })
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeShortSerializer(
            instance.recipe, context=context).data
