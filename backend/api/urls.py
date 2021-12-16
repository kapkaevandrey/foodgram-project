from django.urls import include, path
from rest_framework import routers

from .views import (TagViewSet, RecipeViewSet, IngredientTypeViewSet, IngredientGetViewSet)

router_v1 = routers.DefaultRouter()
router_v1.register('tags', TagViewSet, basename='tags')
router_v1.register('recipes', RecipeViewSet, basename='recipes')
router_v1.register('ingredients', IngredientTypeViewSet, basename='ingredients')

urlpatterns = [
    path('', include(router_v1.urls))
]
