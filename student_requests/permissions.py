from rest_framework import permissions
from users.models import DeputyEducational

class IsStudent(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.parser_context['kwargs']['pk'] == request.user.id)


    def has_object_permission(self, request, view, obj):
        return (request.parser_context['kwargs']['pk'] == request.user.id)
    
class IsDeputyEducational(permissions.BasePermission):
    def has_permission(self, request, view):
        return isinstance(request.user, DeputyEducational)


    def has_object_permission(self, request, view, obj):
        return isinstance(request.user, DeputyEducational)