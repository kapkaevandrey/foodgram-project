import django_filters
from django_filters.rest_framework import CharFilter, FilterSet, MultipleChoiceFilter

from recipes.models import Recipe, IngredientType


class RecipeFilter(FilterSet):
    tags = CharFilter(field_name='tags__slug')

    class Meta:
        model = Recipe
        fields = ['tags']


class IngredientTypeFilter(FilterSet):
    name = CharFilter(
        field_name='name',
        lookup_expr='istartswith'
    )

    class Meta:
        model = IngredientType
        fields = {'name': ['istartswith', 'icontains']}
