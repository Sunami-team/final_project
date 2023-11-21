from users.models import Student, DeputyEducational
from rest_framework import permissions


class IsDeputyEducational(permissions.BasePermission):
    """
    Custom permission to only allow access to Deputy Educational users.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and is a Deputy Educational
        return (
            request.user.is_authenticated
            and request.user.user_type == "deputy_educational"
        )


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        # This checks if the user is authenticated and if their user_type is 'student'
        return request.user.is_authenticated and request.user.user_type == "student"

    def has_object_permission(self, request, view, obj):
        return request.user.is_student and obj.student_id == request.user.id
