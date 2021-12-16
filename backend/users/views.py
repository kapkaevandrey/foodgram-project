from rest_framework import mixins, viewsets, filters
from djoser.views import UserViewSet

from .models import Follow


class CustomUserViewSets(UserViewSet):
    pass