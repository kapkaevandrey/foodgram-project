from rest_framework import viewsets

from .serializers import TagSerializer
from recipes.models import Tag


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()

