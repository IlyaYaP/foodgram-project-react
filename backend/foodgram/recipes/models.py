from tabnanny import verbose
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint

User = get_user_model()

class Recipe(models.Model):
    """ Модель рецепта. """

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта',
    )
    name = models.CharField(
        'Название рецепта',
        max_length=200
    )
    image = models.ImageField(
        'Изоброжение',
        upload_to='recipes/images/'
    )
    description = models.TextField(
        'Описание рецепта'
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления'
    )
    pub_date = models.DateField(
        'Время публикации',
        auto_now_add=True,
    )
    ingredients = models.ManyToManyField(
        'Ingredients',
        through='RecipeIngredient',
        verbose_name='Ингредиенты'
    )    
    tags = models.ManyToManyField(
        'Tag',
        through='RecipeTag',
        verbose_name='Теги',
        related_name='tags'
    )
    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(
        'Тег',
        max_length=200,
        unique=True
    )
    color = models.CharField(
        'Цвет',
        max_length=7,
        unique=True
    )
    slug = models.SlugField(
        'Slug',
        max_length=200,
        unique=True
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
    
    def __str__(self):
        return self.name

class Ingredients(models.Model):

    name = models.CharField(
        'Название',
        max_length=100
    )
    measurement_unit = models.CharField(
        'Единици измерения',
        max_length=200
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

class RecipeIngredient(models.Model):

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    amount = models.IntegerField(
        'Количество',
        validators=[MinValueValidator(1)]
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredient'
            )
        ]

class RecipeTag(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name='Тег'
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['recipe', 'tag'],
                name='unique_recipe_tag'
        )
    ]

class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='shopping_list'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='shopping_list'
    )

    class Meta:
        verbose_name='Лист покупок'
        constraints = [
            UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_user_shoppinglis'
            )
    ]

class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='favorites',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='favorites',
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_user_favorite'
            )
    ]