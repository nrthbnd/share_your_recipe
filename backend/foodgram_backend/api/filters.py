import django_filters
from django_filters import rest_framework as filters
from recipes.models import Ingredients, Recipes, Tags


class IngredientsFilter(filters.FilterSet):
    """Определяет фильтры для модели Ingredients:
    name по строке без учета регистра."""
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Ingredients
        fields = ['name']


class RecipesFilter(filters.FilterSet):
    """Определяет фильтры для рецептов:
    по тегам, по избранному, по списку покупок."""
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tags.objects.all()
    )
    is_favorited = django_filters.BooleanFilter(
        field_name='favorite_recipes',
        method='filter_favorites'
    )
    is_in_shopping_cart = django_filters.BooleanFilter(
        field_name='shopping_cart',
        method='filter_shopping_cart'
    )

    class Meta:
        model = Recipes
        fields = ('tags', 'author',)

    def filter_favorites(self, queryset, name, value):
        return queryset.filter(
            favorites__user=self.request.user) if value else queryset

    def filter_shopping_cart(self, queryset, name, value):
        return queryset.filter(
            shoppinglist__user=self.request.user) if value else queryset
