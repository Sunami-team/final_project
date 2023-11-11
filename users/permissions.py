from rest_framework import permissions
from .models import ITManager, DeputyEducational, Professor, Student


class IsItManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return isinstance(request.user, ITManager)

    def has_object_permission(self, request, view, obj):
        return isinstance(request.user, ITManager)


class IsDeputyEducational(permissions.BasePermission):
    def has_permission(self, request, view):
        return isinstance(request.user, DeputyEducational)

    def has_object_permission(self, request, view, obj):
        return isinstance(request.user, DeputyEducational)


class IsProfessor(permissions.BasePermission):
    def has_permission(self, request, view):
        return isinstance(request.user, Professor)

    def has_object_permission(self, request, view, obj):
        return isinstance(request.user, Professor)


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return isinstance(request.user, Student)

    def has_object_permission(self, request, view, obj):
        return isinstance(request.user, Student)




