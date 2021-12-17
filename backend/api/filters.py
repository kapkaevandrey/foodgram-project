from django_filters.rest_framework import CharFilter, FilterSet, MultipleChoiceFilter

from recipes.models import Recipe


class RecipeFilter(FilterSet):
    tags = CharFilter(field_name='tags__slug')

    class Meta:
        model = Recipe
        fields = ['tags']
