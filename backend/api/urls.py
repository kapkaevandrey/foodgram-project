from django.urls import include, path
from rest_framework import routers
from .users_views import CustomUserViewSets

from .views import (TagViewSet, RecipeViewSet, IngredientTypeViewSet)

router_users = routers.DefaultRouter()
router_v1 = routers.DefaultRouter()
router_users.register("users", CustomUserViewSets, basename='users')
router_v1.register('tags', TagViewSet, basename='tags')
router_v1.register('recipes', RecipeViewSet, basename='recipes')
router_v1.register('ingredients', IngredientTypeViewSet,
                   basename='ingredients')

auth_users = [
    path('', include(router_users.urls)),
    path(r'auth/', include('djoser.urls.authtoken'))
]

urlpatterns = [
    path('', include(router_v1.urls)),
    path('', include(auth_users))
]
