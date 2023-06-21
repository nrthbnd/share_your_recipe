from django_filters import rest_framework as filters

from recipes.models import Ingredients


class IngredientsFilter(filters.FilterSet):
    """Определяет фильтры для модели Ingredients:
    name по строке без учета регистра."""
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Ingredients
        fields = ['name']
