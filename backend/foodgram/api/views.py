from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from requests import Response
from rest_framework import status, viewsets


from recipes.models import (Recipe, Ingredients, RecipeIngredient,
                            Favourite, ShoppingList, Tag)
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .filters import IngredientFilter, RecipeFilter
from .pagination import CustomPagination
from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from api.serializers import (RecipeCreateSerializer, RecipeShortSerializer,
                          IngredientSerializer, RecipeShowSerializer, TagSerializer)


class RecipeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthorOrReadOnly | IsAdminOrReadOnly,]
    pagination_class = CustomPagination
    queryset = Recipe.objects.all()
    filter_backends = [DjangoFilterBackend,]
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeShowSerializer
        return RecipeCreateSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context
    
    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk):
        if request.method == 'POST':
            return self.add(Favourite, request.user, pk)
        else:
            return self.delete(Favourite, request.user, pk)
    
    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def shopping_list(self, request, pk):
        if request.method == 'POST':
            return self.add(ShoppingList, request.user, pk)
        else:
            return self.delete(ShoppingList, request.user, pk)
    
    def add(self, model, user, pk):
        if model.objects.filter(user=user, recipe__id=pk).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        recipe = get_object_or_404(Recipe, id=pk)
        model.objects.create(user=user, recipe=recipe)
        serializer = RecipeShortSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def delete(self, model, user, pk):
        obj = model.objects.filter(user=user, recipe__id=pk)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    @action(
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_list(self, request):
        ingredient_list = 'Список покупок:'
        ingredients = RecipeIngredient.objects.filter(
            recipe__shopping_list__user=request.user
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))
        for num, i in enumerate(ingredients):
            ingredient_list += (
                f"\n{i['ingredient__name']} - "
                f"{i['amount']} {i['ingredient__measurement_unit']}"
            
            )
            if num < ingredients.count() - 1:
                ingredient_list += ', '
        file = 'shopping_list'
        response = HttpResponse(ingredient_list, 'Content-Type: application/pdf')
        response['Contetnt-Disposition'] = f'attachment; filename="{file}.pdf"'
        return response 




class TagViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAdminOrReadOnly,]
    pagination_class = None
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAdminOrReadOnly,]
    pagination_class = None
    serializer_class = IngredientSerializer
    queryset = Ingredients.objects.all()
    filter_backends = [DjangoFilterBackend,]
    filterset_class = IngredientFilter
    search_fields = ['^name',]

