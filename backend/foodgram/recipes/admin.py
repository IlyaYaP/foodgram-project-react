from django.contrib import admin

from .models import Recipe, Ingredients, ShoppingList, Tag, Favorite, User


class IngredientsInLine(admin.TabularInline):
    model = Recipe.ingredients.through

#admin.site.register(User)
admin.site.register(Recipe)
admin.site.register(Ingredients)
admin.site.register(ShoppingList)
admin.site.register(Tag)
admin.site.register(Favorite)