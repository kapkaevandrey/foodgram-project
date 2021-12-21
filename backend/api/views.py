from django.conf import settings
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from recipes.models import Ingredient, IngredientType, Recipe, Tag

from .filters import IngredientTypeFilter, RecipeFilter
from .pagination import PageNumberLimitPagination
from .permissions import AdminOrReadOnly, AuthorAdminOrReadOnly
from .serializers import (IngredientTypeSerializer, RecipeGetSerializer,
                          RecipeSerializer, RecipeSimpleSerializer,
                          TagSerializer)


class TagViewSet(mixins.RetrieveModelMixin,
                 mixins.ListModelMixin,
                 viewsets.GenericViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    pagination_class = None
    permission_classes = (AdminOrReadOnly,)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (AuthorAdminOrReadOnly,)
    pagination_class = PageNumberLimitPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('author__id',)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return RecipeGetSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return Recipe.objects.all()
        fav_param_value = self.request.query_params.get('is_favorited')
        shop_param_value = self.request.query_params.get(
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

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = False
        return self.update(request, *args, **kwargs)

    @action(methods=['get', 'delete'], detail=True,
            permission_classes=[permissions.IsAuthenticated])
    def favorite(self, request, pk=None):
        recipe = get_object_or_404(Recipe, id=pk)
        user = request.user
        recipe_exist = user in recipe.recipe_followers.all()
        if request.method == 'DELETE':
            if not recipe_exist:
                return Response(
                    {"errors": _(
                        'This recipe is not on your favorites list'
                    )},
                    status=status.HTTP_400_BAD_REQUEST)
            recipe.recipe_followers.remove(user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        if recipe_exist:
                return Response(
                    {"errors": _(
                        'This recipe is already in the favorites list'
                    )},
                    status=status.HTTP_400_BAD_REQUEST)
        recipe.recipe_followers.add(user)
        serializer = RecipeSimpleSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['get', 'delete'], detail=True,
            permission_classes=[permissions.IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        recipe = get_object_or_404(Recipe, id=pk)
        user = request.user
        recipe_exist = user in recipe.shop_followers.all()
        if request.method == 'DELETE':
            if not recipe_exist:
                return Response(
                    {"errors": _('This recipe is not on your shopping list')},
                    status=status.HTTP_400_BAD_REQUEST)
            recipe.shop_followers.remove(user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        if recipe_exist:
            return Response(
                    {'errors': _(
                        'This recipe is already in the shopping list'
                    )},
                    status=status.HTTP_400_BAD_REQUEST)
        recipe.shop_followers.add(user)
        recipe.save()
        serializer = RecipeSimpleSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['get'], detail=False,
            permission_classes=[permissions.IsAuthenticated], )
    def download_shopping_cart(self, request):
        recipes = request.user.shopping_list.all()
        if len(recipes) == 0:
            return Response(status=status.HTTP_204_NO_CONTENT)
        ingredients = Ingredient.objects.filter(recipe__in=recipes)
        data = {}
        for ingredient in ingredients:
            if ingredient.type.__str__() not in data:
                data[ingredient.type.__str__()] = 0
            data[ingredient.type.__str__()] += ingredient.amount
        with open(
                f"{settings.BASE_DIR}/media/shopping_list.txt",
                "w", encoding="utf8") as file:
            for key, value in data.items():
                file.write(f"{key.capitalize()} - {value}\n")
        return FileResponse(
            open(f"{settings.BASE_DIR}/media/shopping_list.txt", "rb")
        )


class IngredientTypeViewSet(viewsets.ModelViewSet):
    queryset = IngredientType.objects.all()
    serializer_class = IngredientTypeSerializer
    pagination_class = None
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientTypeFilter
