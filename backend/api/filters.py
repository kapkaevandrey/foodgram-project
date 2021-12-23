from django_filters.rest_framework import (CharFilter, FilterSet,
                                           ModelMultipleChoiceFilter)
from django.conf import settings

from recipes.models import IngredientType, Recipe, Tag


class RecipeFilter(FilterSet):
    tags = ModelMultipleChoiceFilter(field_name='tags__slug',
                                     lookup_expr='exact',
                                     to_field_name='slug',
                                     queryset=Tag.objects.all())

    class Meta:
        model = Recipe
        fields = ['tags']

    @staticmethod
    def favorite_and_shopping_cart(request):
        user = request.user
        if user.is_anonymous:
            return Recipe.objects.all()
        fav_param_value = request.query_params.get('is_favorited')
        shop_param_value = request.query_params.get(
            'is_in_shopping_cart'
        )
        is_favorite = (fav_param_value in
                       settings.URLS_VALID_VALUE_PARAMS['True'])
        in_shop_cart = (shop_param_value in
                        settings.URLS_VALID_VALUE_PARAMS['True'])
        if is_favorite and in_shop_cart:
            return user.favorite_recipes.all() & user.shopping_list.all()
        elif in_shop_cart:
            return user.shopping_list.all()
        elif is_favorite:
            return user.favorite_recipes.all()
        return Recipe.objects.all()


class IngredientTypeFilter(FilterSet):
    name = CharFilter(
        field_name='name',
        lookup_expr='istartswith'
    )

    class Meta:
        model = IngredientType
        fields = ['name']
