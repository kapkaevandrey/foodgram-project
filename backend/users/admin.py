from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Follow


class MyUserAdmin(UserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1',
                       'password2', 'first_name', 'last_name')}
         ),
    )


admin.site.register(User, MyUserAdmin)
admin.site.register(Follow)
