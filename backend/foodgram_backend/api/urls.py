from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (IngredientsViewSet, RecipesInCartViewSet, RecipesViewSet,
                    TagsViewSet)

app_name = 'api'
router = DefaultRouter()

router.register(r'tags', TagsViewSet, basename='tags')
router.register(r'recipes', RecipesViewSet, basename='recipes')
router.register(
    r'recipes/(?P<recipe_id>\d+)/shopping_cart',
    RecipesInCartViewSet,
    basename='shopping_cart',
)
router.register(r'ingredients', IngredientsViewSet, basename='ingredients')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
]
