from rest_framework import mixins, viewsets, filters


from .serializers import FollowSerializer
from .models import Follow


class FollowViewSets(viewsets.ReadOnlyModelViewSet,
                     mixins.CreateModelMixin,
                     mixins.DestroyModelMixin):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("following__username",)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# TODO работа с endpoints