from django_filters.rest_framework import (AllValuesMultipleFilter, CharFilter,
                                           FilterSet)

from recipes.models import IngredientType, Recipe


class RecipeFilter(FilterSet):
    tags = AllValuesMultipleFilter(field_name='tags__slug', lookup_expr='exact')

    class Meta:
        model = Recipe
        fields = ['tags__slug']


class IngredientTypeFilter(FilterSet):
    name = CharFilter(
        field_name='name',
        lookup_expr='istartswith'
    )

    class Meta:
        model = IngredientType
        fields = ['name']
