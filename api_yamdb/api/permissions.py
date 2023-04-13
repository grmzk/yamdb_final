from rest_framework import permissions


class IsAdminOrSuperUser(permissions.BasePermission):
    """
    Только админу доступны все действия со всеми профилями,
    Django SuperUser приравнивается к админу.
    """

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.is_admin
                     or (request.user.is_staff and request.user.is_superuser)))


class IsSuperUserIsAdminIsModeratorIsAuthor(permissions.BasePermission):
    """
    Анонимный пользователь может совершать только безопасные запросы.
    Доступ к запросам PATCH и DELETE предоставляется только
    суперпользователю, админу, аутентифицированным пользователям
    с ролью admin или moderator, а также автору объекта.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and ((request.user.is_staff and request.user.is_superuser)
                 or request.user.is_admin
                 or request.user.is_moderator
                 or request.user == obj.author)
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """Класс разрешений для админа или для всех пользователей на чтение."""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and (request.user.is_admin
                         or (request.user.is_staff
                             and request.user.is_superuser))))
