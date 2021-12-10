from django.contrib.auth.models import AbstractUser
from django.db import models

from django.utils.translation import gettext as _


class User(AbstractUser):
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']


class Follow(models.Model):
    user = models.ForeignKey(User, related_name='follower',
                             on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='following',
                               on_delete=models.CASCADE)

    def __str__(self):
        return _('{user} follow to {author}').format(user=self.user, author=self.author)

    class Meta:
        ordering = ['user']
        verbose_name = _('Follow')
        verbose_name_plural = _('Follows')
        constraints = [models.UniqueConstraint(
            fields=["user", "author"], name="unique follow"
        )]


User._meta.get_field('email').blank = False
User._meta.get_field('last_name').blank = False
User._meta.get_field('first_name').blank = False


