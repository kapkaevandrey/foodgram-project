from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from recipes.models import IngredientType, Recipe, Tag
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
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return RecipeGetSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        return self.filterset_class.favorite_and_shopping_cart(self.request)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = False
        return self.update(request, *args, **kwargs)

    @action(methods=['get', 'delete'], detail=True,
            permission_classes=[permissions.IsAuthenticated])
    def favorite(self, request, pk=None):
        recipe = get_object_or_404(Recipe, id=pk)
        user = request.user
        recipe_exist = recipe.recipe_followers.filter(
            favoriterecipe__user=user).exists()
        if request.method == 'DELETE':
            if not recipe_exist:
                return Response(
                    {'errors': _(
                        'This recipe is not on your favorites list'
                    )},
                    status=status.HTTP_400_BAD_REQUEST)
            recipe.recipe_followers.remove(user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        if recipe_exist:
            return Response(
                {'errors': _('This recipe is already in the favorites list')},
                status=status.HTTP_400_BAD_REQUEST)
        recipe.recipe_followers.add(user)
        serializer = RecipeSimpleSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['get', 'delete'], detail=True,
            permission_classes=[permissions.IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        recipe = get_object_or_404(Recipe, id=pk)
        user = request.user

        recipe_exist = recipe.shop_followers.filter(
            shoppinglist__user=user).exists()
        if request.method == 'DELETE':
            if not recipe_exist:
                return Response(
                    {'errors': _('This recipe is not on your shopping list')},
                    status=status.HTTP_400_BAD_REQUEST)
            recipe.shop_followers.remove(user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        if recipe_exist:
            return Response(
                {'errors': _('This recipe is already in the shopping list')},
                status=status.HTTP_400_BAD_REQUEST)
        recipe.shop_followers.add(user)
        recipe.save()
        serializer = RecipeSimpleSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['get'], detail=False,
            permission_classes=[permissions.IsAuthenticated], )
    def download_shopping_cart(self, request):
        recipes = request.user.shopping_list.all()
        if recipes.count() == 0:
            return Response(status=status.HTTP_204_NO_CONTENT)
        shopp_list = recipes.values_list(
            'ingredients__type__name',
            'ingredients__type__measurement_unit').annotate(
            ammount_sum=Sum("ingredients__amount")).order_by(
            'ingredients__type__name')
        data = "\n".join([f"{name} ({mou}) - {amount}"
                          for name, mou, amount in shopp_list])
        response = HttpResponse(data, content_type="text/plain,charset=utf8")
        response['Content-Disposition'] = 'attachment; filename=shopping list'
        return response


class IngredientTypeViewSet(viewsets.ModelViewSet):
    queryset = IngredientType.objects.all()
    serializer_class = IngredientTypeSerializer
    pagination_class = None
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientTypeFilter
