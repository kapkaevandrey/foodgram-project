from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']


User._meta.get_field('email').blank = False
User._meta.get_field('last_name').blank = False
User._meta.get_field('first_name').blank = False


