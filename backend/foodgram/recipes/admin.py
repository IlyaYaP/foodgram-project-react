from django.contrib import admin

from foodgram.settings import EMPTY

from .models import Recipe, Ingredients, ShoppingList, Tag, Favorite


class IngredientsInLine(admin.TabularInline):
    model = Recipe.ingredients.through
