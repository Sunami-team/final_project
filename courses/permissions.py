from rest_framework import permissions
from users.models import ITManager

class IsItManager(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return isinstance(request.user, ITManager)

    def has_object_permission(self, request, view, obj):
        return isinstance(request.user, ITManager)