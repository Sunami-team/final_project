from rest_framework import permissions
from users.models import ITManager, Student


class IsItManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return isinstance(request.user, ITManager)

    def has_object_permission(self, request, view, obj):
        return isinstance(request.user, ITManager)


def has_user_type_permission(user, user_type):
    return user.user_type == user_type


class IsAdminOrEducationalDeputyOrAdvisor(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        student_id = view.kwargs.get('pk')
        if student_id == 'me':
            student_id = user.pk

        if user.is_superuser:
            return True

        if hasattr(user, 'professor') or hasattr(user, 'deputyeducational'):
            student = Student.objects.get(pk=student_id)
            if hasattr(user, 'professor') and user.professor.faculty == student.college:
                return True
            if hasattr(user, 'deputyeducational') and user.deputyeducational.faculty == student.college:
                return True

        return False
