from tabnanny import verbose
from turtle import color
from django.db import models
from django.contrib.auth import get_user_model

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

    #ingredients = models.ManyToManyField(
        
    #tags = 

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