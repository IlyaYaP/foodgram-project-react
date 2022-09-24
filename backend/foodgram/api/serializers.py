from dataclasses import field, fields
from imp import source_from_cache
from pyexpat import model
from urllib import request
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import (Favorite, Ingredients, Recipe, RecipeIngredient,
                            RecipeTag, ShoppingList,Tag)
from users.models import User, Subscription
from djoser.serializers import UserCreateSerializer, UserSerializer



class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscrided'
        ]

    def get_is_subscrided(self, obj):
        request = self.context.get('request')
        if request in None or request.user.is_anonymous:
            return False
        return Subscription.objects.filter(
            user=request.user, author=obj
        ).exists()


class CustomUserCreateSerializer(UserCreateSerializer):

    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        ]

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = [
            'id',
            'name',
            'color',
            'slug'
        ]

class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredients
        fields = [
            'id',
            'name',
            'measurement_unit'
        ]


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField(
        method_name='get_is_favorited')
    is_in_shopping_list = serializers.SerializerMethodField(
        method_name='get_is_in_shopping_list')

    class Meta:
        model = Recipe
        fields = [
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_list',
            'name',
            'image',
            'text',
            'cooking_time'
        ]
    
    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return Favorite.objects.filter(
            user=request.user, recipe_id=obj
        ).exists()

    def get_is_in_shopping_list(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return ShoppingList.objects.filter(
            user=request.user, recipe_id=obj
        ).exists()


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = ['id', 'name', 'amount', 'measurement_unit']
