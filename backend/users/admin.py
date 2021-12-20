from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Follow, User


class MyUserAdmin(UserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1',
                       'password2', 'first_name', 'last_name')}
         ),
    )
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'email', 'username')


admin.site.register(User, MyUserAdmin)
admin.site.register(Follow)
