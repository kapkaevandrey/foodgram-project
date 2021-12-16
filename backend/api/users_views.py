from rest_framework import mixins, viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from djoser.views import UserViewSet
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

from .serializers import GetUserSerializer

User = get_user_model()


class CustomUserViewSets(UserViewSet):
    @action(methods=['get', 'delete'], detail=True,
            permission_classes=[IsAuthenticated])
    def subscribe(self, request, id=None):
        user = get_object_or_404(User, id=id)
        if user == request.user:
            return Response(
                {"errors": _('Don\'t subscribe (delete) to yourself!')},
                status=status.HTTP_400_BAD_REQUEST
            )
        if request.method == 'DELETE':
            if user not in request.user.subscribers.all():
                return Response(
                    {"errors": _('This author is not in your subscriptions')},
                    status=status.HTTP_400_BAD_REQUEST)
            request.user.subscribers.remove(user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        if user in request.user.subscribers.all():
            return Response(
                {"errors": _('You have already subscribed to this author')},
                status=status.HTTP_400_BAD_REQUEST
            )
        request.user.subscribers.add(user)
        serializer = GetUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated],
            pagination_class=PageNumberPagination)
    def subscriptions(self, request):
        subscribers = request.user.subscribers.all()
        serializer = GetUserSerializer(subscribers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
