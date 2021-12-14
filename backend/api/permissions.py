from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):
    """Фильтр - разрешает GET запросы всем, остальное только для ADMIN"""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.is_admin))


class AuthorAdminOrReadOnly(permissions.BasePermission):
    """Разрешение на чтение для всех пользователей.
    Редактирование, обновление или удаление разрешено только
    авторам и администраторам."""

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and (obj.author == request.user
                         or request.user.is_admin)))


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_admin)
