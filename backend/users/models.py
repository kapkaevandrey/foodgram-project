from django.contrib.auth.models import AbstractUser
from django.core.validators import ValidationError
from django.db import models
from django.utils.translation import gettext as _


class User(AbstractUser):
    email = models.EmailField(_('email address'), blank=False, unique=True)
    subscribers = models.ManyToManyField('User', through='Follow')

    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']
    USERNAME_FIELD = 'email'

    @property
    def is_admin(self):
        return (
            self.is_superuser
            or self.is_staff)

    def __str__(self):
        return self.username


class Follow(models.Model):
    user = models.ForeignKey(User, related_name='users',
                             on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='authors',
                               on_delete=models.CASCADE)

    def clean(self):
        if self.user == self.author:
            raise ValidationError(
                _('You can\'t subscribe to yourself')
            )

    class Meta:
        ordering = ['user']
        verbose_name = _('Follow')
        verbose_name_plural = _('Follows')
        constraints = [models.UniqueConstraint(
            fields=["user", "author"], name="unique follow"
        )]

    def __str__(self):
        return _('{user} follow to {author}').format(user=self.user,
                                                     author=self.author)


User._meta.get_field('last_name').blank = False
User._meta.get_field('first_name').blank = False
