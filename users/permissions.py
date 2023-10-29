from rest_framework import permissions

from .models import *


class IsProfessor(permissions.BasePermission):

    def has_permission(self, request, view):
        return Professor.objects.filter(user=request.user).exists()


class IsStudent(permissions.BasePermission):

    def has_permission(self, request, view):
        return Student.objects.filter(user=request.user).exists()


class IsITManager(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return isinstance(request.user, ITManager)


class IsDeputyEducational(permissions.BasePermission):

    def has_permission(self, request, view):
        return DeputyEducational.objects.filter(user=request.user).exists()
