from rest_framework import viewsets, permissions

from .serializers import (TagSerializer, RecipeSimpleSerializer,
                          RecipeGetSerializer, RecipeSerializer, IngredientTypeSerializer, IngredientSerializer)
from recipes.models import Tag, Recipe, IngredientType, Ingredient


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()

    def get_serializer_class(self):
        if self.request.method not in permissions.SAFE_METHODS:
            return RecipeSerializer
        return RecipeGetSerializer


    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = IngredientType.objects.all()
    serializer_class = IngredientTypeSerializer


class IngredientGetViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer




