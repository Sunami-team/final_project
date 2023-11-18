from rest_framework.permissions import BasePermission

class IsStudentOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_student

    def has_object_permission(self, request, view, obj):
        return request.user.is_student and obj.student_id == request.user.id
    