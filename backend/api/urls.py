from django.urls import include, path
from rest_framework import routers

from .views import (TagViewSet, RecipeViewSet, IngredientViewSet, IngredientGetViewSet)

router_v1 = routers.DefaultRouter()
router_v1.register('tags', TagViewSet, basename='tags')
router_v1.register('recipes', RecipeViewSet, basename='recipes')
router_v1.register('ingredients', IngredientViewSet, basename='ingredients')
router_v1.register('ingredients123', IngredientGetViewSet, basename='ingredients132')

urlpatterns = [
    path('', include(router_v1.urls))
]
