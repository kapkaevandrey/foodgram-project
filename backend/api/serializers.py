from django.conf import settings
from rest_framework import serializers

from recipes.models import Tag

class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Tag"""
    class Meta:
        model = Tag
        fields = '__all__'
