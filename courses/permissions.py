from rest_framework import permissions
from users.models import ITManager


class IsItManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return isinstance(request.user, ITManager)

    def has_object_permission(self, request, view, obj):
        return isinstance(request.user, ITManager)


def has_user_type_permission(user, user_type):
    return user.user_type == user_type
