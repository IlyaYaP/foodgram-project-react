from django_filters.rest_framework import FilterSet
from django_filters.rest_framework.filters import (AllValuesMultipleFilter,
                                                   BooleanFilter)
from recipes.models import Recipe
from rest_framework.filters import SearchFilter


class IngredientSearchFilter(SearchFilter):
    search_param = 'name'


class RecipeFilterSet(FilterSet):
    tags = AllValuesMultipleFilter(
        field_name='tags__slug',)
    is_favorited = BooleanFilter(method='get_is_favorited')
    is_in_shopping_cart = BooleanFilter(
        method='get_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart')

    def get_is_favorited(self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            return queryset.filter(in_favorite__user=self.request.user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            return queryset.filter(shoppingcart__user=self.request.user)
        return queryset.all()
