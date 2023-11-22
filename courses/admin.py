from django.contrib import admin

from users.models import DeputyEducational, ITManager
from .models import Course, CourseTerm, StudentCourse, Term, Faculty, StudyField
from .permissions import has_user_type_permission


# admin.site.register(Course)
# admin.site.register(CourseTerm)
# admin.site.register(StudentCourse)
# admin.site.register(Term)
# admin.site.register(Faculty)
# admin.site.register(StudyField)


class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'course_unit', 'course_type')
    search_fields = ('name', 'faculty__name')
    #filter_horizontal = ('faculty', 'pre_requisites', 'co_requisites')

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return has_user_type_permission(request.user, "DeputyEducational") or has_user_type_permission(request.user,
                                                                                                       "ITManager")




admin.site.register(Course, CourseAdmin)


class CourseTermAdmin(admin.ModelAdmin):
    list_display = ('course', 'class_day', 'class_time', 'exam_date_time')
    search_fields = ('course__name', 'professor__name')
    list_filter = ('class_day', 'term')

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return has_user_type_permission(request.user, "DeputyEducational") or has_user_type_permission(request.user,
                                                                                                       "ITManager")




admin.site.register(CourseTerm, CourseTermAdmin)


class StudentCourseAdmin(admin.ModelAdmin):
    list_display = ('student', 'course_term', 'grade')
    search_fields = ('student__first_name', 'student__last_name', 'course_term__course__name')
    list_filter = ['term']

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return has_user_type_permission(request.user, "DeputyEducational") or has_user_type_permission(request.user,
                                                                                                       "ITManager")



admin.site.register(StudentCourse, StudentCourseAdmin)


class TermAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_classes', 'end_classes')
    search_fields = ('name',)
    list_filter = ('start_classes', 'end_classes')

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return has_user_type_permission(request.user, "DeputyEducational") or has_user_type_permission(request.user,
                                                                                                       "ITManager")




admin.site.register(Term, TermAdmin)


class FacultyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return has_user_type_permission(request.user, "DeputyEducational") or has_user_type_permission(request.user,
                                                                                                       "ITManager")



admin.site.register(Faculty, FacultyAdmin)


class StudyFieldAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'total_units')
    search_fields = ('name', 'faculty__name')
    list_filter = ('level',)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return has_user_type_permission(request.user, "DeputyEducational") or has_user_type_permission(request.user,
                                                                                                       "ITManager")



admin.site.register(StudyField, StudyFieldAdmin)
