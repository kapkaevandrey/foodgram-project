from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from djoser.serializers import UserSerializer

from rest_framework import serializers

from .models import Follow

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField(required=False, read_only=True)

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, author=obj).exists()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed')
        read_only_fields = ('username', 'email')


# class FollowSerializer(serializers.ModelSerializer):
#     user = serializers.SlugRelatedField(
#         slug_field="username", read_only=True,
#         default=serializers.CurrentUserDefault())
#     following = serializers.SlugRelatedField(
#         slug_field="username",
#         queryset=User.objects.all())
#
#     class Meta:
#         model = Follow
#         fields = ("user", "following")
#         validators = [
#             serializers.UniqueTogetherValidator(
#                 queryset=Follow.objects.all(),
#                 fields=("following", "user")
#             )
#         ]
#
#     def validate_following(self, value):
#         user = self.context["request"].user
#         if value == user:
#             raise serializers.ValidationError(
#                 _('Don\'t subscribe to yourself')
#             )
#         return value
