from django_filters.rest_framework import CharFilter, FilterSet, AllValuesMultipleFilter

from recipes.models import Recipe, IngredientType


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
