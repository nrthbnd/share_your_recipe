from django_filters import rest_framework as filters

from recipes.models import Ingredients, Recipes, Tags
from users.models import User


class IngredientsFilter(filters.FilterSet):
    """Определяет фильтры для модели Ingredients:
    name по строке без учета регистра."""
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Ingredients
        fields = ['name']


class RecipesFilter(filters.FilterSet):
    """Определяет фильтры для рецептов:
    по тегам, автору, по избранному, по списку покупок."""
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tags.objects.all()
    )
    author = filters.ModelChoiceFilter(
        field_name='author_id',
        queryset=User.objects.all()
    )
    is_favorited = filters.BooleanFilter(
        field_name='favorite_recipes',
        method='filter_favorites'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        field_name='shopping_cart',
        method='filter_shopping_cart'
    )

    class Meta:
        model = Recipes
        fields = ('tags', 'author')
        # 'is_favorited', 'is_in_shopping_cart'

    def filter_favorites(self, queryset, name, value):
        return (queryset.filter(
            in_favorites__user=self.request.user) if (
            value and self.request.user.is_authenticated) else queryset)

    def filter_shopping_cart(self, queryset, name, value):
        return queryset.filter(
            in_shopping_cart__user=self.request.user) if value else queryset
