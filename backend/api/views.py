from rest_framework import viewsets, permissions

from recipes.models import Tag, Recipe, IngredientType, Ingredient

from .serializers import (TagSerializer, RecipeSimpleSerializer,
                          RecipeGetSerializer, RecipeSerializer, IngredientTypeSerializer, IngredientSerializer)
from .permissions import AuthorAdminOrReadOnly, AdminOrReadOnly

class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (AuthorAdminOrReadOnly,
                          AdminOrReadOnly)

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return RecipeGetSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = False
        return self.update(request, *args, **kwargs)



class IngredientViewSet(viewsets.ModelViewSet):
    queryset = IngredientType.objects.all()
    serializer_class = IngredientTypeSerializer


class IngredientGetViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer




