from rest_framework import permissions
from .models import ITManager, DeputyEducational, Professor, Student, User


def has_user_type_permission(user, user_type):
    return user.user_type == user_type


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


class IsStudentOrDeputyEducational(permissions.BasePermission):
    """
    Educational Deputy and certain Student allowed
    """

    def has_permission(self, request, view):
        if (
                (
                        view.request.method == "PUT"
                        or view.request.method == "PATCH"
                        or view.request.method == "GET"
                )
                and isinstance(request.user, User)
                and request.user.is_student
        ):
            return True
        elif (
                view.request.method == "GET"
                and isinstance(request.user, User)
                and request.user.is_deputy_educational
        ):
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if isinstance(request.user, User):
            return request.user.id == obj.id or request.user.is_deputy_educational
        return False


class IsProfessorOrDeputyEducational(permissions.BasePermission):
    """
    Educational Deputy and certain Professor allowed
    """

    def has_permission(self, request, view):
        if (
                (
                        view.request.method == "PUT"
                        or view.request.method == "PATCH"
                        or view.request.method == "GET"
                )
                and isinstance(request.user, User)
                and request.user.is_professor
        ):
            return True
        elif (
                view.request.method == "GET"
                and isinstance(request.user, User)
                and request.user.is_deputy_educational
        ):
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if isinstance(request.user, User):
            return request.user.id == obj.id or request.user.is_deputy_educational
        return False


class IsItManagerOrDeputyEducational(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.user_type == "it_manager" or user.user_type == "deputy_educational"
