from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from rest_framework import serializers

from .models import Follow

User = get_user_model()


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field="username", read_only=True,
        default=serializers.CurrentUserDefault())
    following = serializers.SlugRelatedField(
        slug_field="username",
        queryset=User.objects.all())

    class Meta:
        model = Follow
        fields = ("user", "following")
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=("following", "user")
            )
        ]

    def validate_following(self, value):
        user = self.context["request"].user
        if value == user:
            raise serializers.ValidationError(
                _('Don\'t subscribe to yourself')
            )
        return value
