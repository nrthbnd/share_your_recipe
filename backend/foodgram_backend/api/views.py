from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import Favorites, Ingredients, Recipes, ShoppingList, Tags
from rest_framework import exceptions, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response

from .filters import IngredientsFilter, RecipesFilter
from .pagination import PageLimitPagination
from .permissions import IsAuthorOrAdminOrReadOnly
from .serializers import (IngredientsSerializer, RecipesMajorSerializer,
                          RecipesReadSerializer, RecipesWriteSerializer,
                          TagsSerializer)


class RecipesViewSet(viewsets.ModelViewSet):
    """Список рецептов."""
    queryset = Recipes.objects.all()
    pagination_class = PageLimitPagination
    permission_classes = (IsAuthorOrAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipesFilter

    def get_serializer_class(self):
        """Выбор сериализатора для рецептов в зависимости от метода."""
        if self.action in SAFE_METHODS:
            return RecipesReadSerializer
        return RecipesWriteSerializer

    def perform_create(self, serializer):
        """Сохранение рецепта с автором."""
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        """Изменение рецепта полностью."""
        serializer.save(author=self.request.user, partial=False)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=(IsAuthenticated,))
    def favorite(self, request, pk=None):
        """Проверяет, добавлен ли рецепт в избранное
        и добавляет/удаляет его."""
        user = self.request.user
        recipe = get_object_or_404(Recipes, pk=pk)

        if self.request.method == 'POST':
            if Favorites.objects.filter(recipe_id=recipe, user=user).exists():
                raise exceptions.ValidationError(
                    'Рецепт уже добавлен в избранное!'
                )
            Favorites.objects.create(recipe_id=recipe, user=user)
            serializer = RecipesMajorSerializer(
                recipe,
                context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if self.request.method == 'DELETE':
            if not Favorites.objects.filter(
                recipe_id=recipe,
                user=user
            ).exists():
                raise exceptions.ValidationError(
                    'Рецепта нет в избранном!'
                )
            favorites = get_object_or_404(Favorites,
                                          recipe_id=recipe,
                                          user=user)
            favorites.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=(IsAuthenticated,))
    def shopping_cart(self, request, pk=None):
        """Проверяет, добавлен ли рецепт в список покупок
        и добавляет/удаляет его."""
        user = self.request.user
        recipe = get_object_or_404(Recipes, pk=pk)

        if self.request.method == 'POST':
            if ShoppingList.objects.filter(
                recipe_id=recipe,
                user=user
            ).exists():
                raise exceptions.ValidationError(
                    'Рецепт уже добавлен в избранное!'
                )
            ShoppingList.objects.create(recipe_id=recipe, user=user)
            serializer = RecipesMajorSerializer(
                recipe,
                context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if self.request.method == 'DELETE':
            if not ShoppingList.objects.filter(
                recipe_id=recipe,
                user=user
            ).exists():

                raise exceptions.ValidationError(
                    'Рецепта нет в списке покупок!'
                )
            in_shopping_cart = get_object_or_404(
                ShoppingList, recipe_id=recipe, user=user,
            )
            in_shopping_cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class IngredientsViewSet(viewsets.ModelViewSet):
    """Список ингредиентов."""
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = (IsAuthorOrAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = IngredientsFilter
    search_fields = ('name',)


class TagsViewSet(viewsets.ModelViewSet):
    """Список тегов длфя рецептов."""
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer


class RecipesInCartViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    serializer_class = RecipesMajorSerializer
    permission_classes = (IsAuthorOrAdminOrReadOnly,)
