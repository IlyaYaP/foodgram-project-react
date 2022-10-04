from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from requests import Response
from rest_framework import status, viewsets
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet



from recipes.models import (Recipe, Ingredients, RecipeIngredient,
                            Favorite, ShoppingList, Tag)
from users.models import Subscription, User
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated

from .filters import IngredientFilters, RecipeFilterSet
from .pagination import CustomPagination
from .permissions import IsAuthorOrAdminOrReadOnly
from .serializers import (RecipeCreateSerializer, FavoriteSerializer,
                          IngredientSerializer, RecipeSerializer,
                          ShoppingListSerializer, ShowSubscriptionSerializers,
                          SubscriptionSerializre, TagSerializer)

class RecipeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthorOrAdminOrReadOnly,]
    pagination_class = CustomPagination
    queryset = Recipe.objects.all()
    filter_backends = [DjangoFilterBackend,]
    filterset_class = RecipeFilterSet

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializer
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
            return self.add(Favorite, request.user, pk)
        else:
            return self.delete(Favorite, request.user, pk)
    
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
        serializer = RecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def delete(self, modelr, user, pk):
        obj = model.objects.filter(user=user, recipe__id=pk)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)




class TagViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny,]
    pagination_class = None
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny,]
    pagination_class = None
    serializer_class = IngredientSerializer
    queryset = Ingredients.objects.all()
    filter_backends = [IngredientFilters,]
    search_fields = ['^name',]

#class FavoriteViewSet(viewsets.ModelViewSet):
