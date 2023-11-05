from rest_framework import permissions, serializers
from .models import ITManager, DeputyEducational
from .models import User, Student, Professor




class IsItManager(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return isinstance(request.user, ITManager)

    def has_object_permission(self, request, view, obj):

        return isinstance(request.user, ITManager)
    

class IsStudentOrDeputyEducational(permissions.BasePermission):
    def has_permission(self, request, view):
        if (view.request.method == 'PUT' or view.request.method == 'PATCH' or view.request.method == 'GET') and isinstance(request.user, User) and request.user.is_student:
            return True
        elif view.request.method == 'GET' and isinstance(request.user, User) and request.user.is_deputy_educational :
            return True
        return False
    
    def has_object_permission(self, request, view, obj):
        if isinstance(request.user, User):
            return request.user.id == obj.id or request.user.is_deputy_educational
        return False

class IsProfessorOrDeputyEducational(permissions.BasePermission):
    def has_permission(self, request, view):
        if (view.request.method == 'PUT' or view.request.method == 'PATCH' or view.request.method == 'GET') and isinstance(request.user, User) and request.user.is_professor:
            return True
        elif view.request.method == 'GET' and isinstance(request.user, User) and request.user.is_deputy_educational :
            return True
        return False
    
    def has_object_permission(self, request, view, obj):
        if isinstance(request.user, User):
            return request.user.id == obj.id or request.user.is_deputy_educational
        return False


class TestMest(permissions.BasePermission):
    def has_permission(self, request, view):
        return True
    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.id


    


class IsDeputyEducational(permissions.BasePermission):
    def has_permission(self, request, view):
        return isinstance(request.user, DeputyEducational)
    