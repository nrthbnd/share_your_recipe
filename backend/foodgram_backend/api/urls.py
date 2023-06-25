from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (IngredientsViewSet, RecipesInCartViewSet, RecipesViewSet,
                    TagsViewSet)

app_name = 'api'
router = DefaultRouter()

router.register('tags', TagsViewSet)
router.register('recipes', RecipesViewSet)
router.register(
    r'recipes/(?P<recipe_id>\d+)/shopping_cart',
    RecipesInCartViewSet,
    basename='shopping_cart',
)
router.register('ingredients', IngredientsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    # path('auth/', include('djoser.urls.authtoken')),
]

# router.register(
# r'recipes/(?P<recipe_id>\d+)/favorite',
# FavoriteViewSet,
# basename='favorite',
# )
