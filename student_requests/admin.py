from django.contrib import admin

from users.models import DeputyEducational, ITManager
from .models import CourseRegistrationRequest, CourseCorrectionRequest, GradeReconsiderationRequest, \
    EmergencyDropRequest, TermDropRequest

from .permissions import has_user_type_permission


# admin.site.register(CourseRegistrationRequest)
# admin.site.register(CourseCorrectionRequest)
# admin.site.register(GradeReconsiderationRequest)
# admin.site.register(EmergencyDropRequest)
# admin.site.register(TermDropRequest)


class CourseRegistrationRequestAdmin(admin.ModelAdmin):
    list_display = ('student', 'approval_status', 'display_requested_courses')
    search_fields = ('student__first_name', 'student__last_name')
    list_filter = ('approval_status',)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return has_user_type_permission(request.user, "DeputyEducational") or has_user_type_permission(request.user,
                                                                                                       "ITManager")

    def display_requested_courses(self, obj):
        return ", ".join([course.name for course in obj.requested_courses.all()])

    display_requested_courses.short_description = 'Requested Courses'


admin.site.register(CourseRegistrationRequest, CourseRegistrationRequestAdmin)


class CourseCorrectionRequestAdmin(admin.ModelAdmin):
    list_display = ('student', 'approval_status', 'display_courses_to_drop', 'display_courses_to_add')
    search_fields = ('student__first_name', 'student__last_name')
    list_filter = ('approval_status',)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return has_user_type_permission(request.user, "DeputyEducational") or has_user_type_permission(request.user,
                                                                                                       "ITManager")

    def display_courses_to_drop(self, obj):
        return ", ".join([course.name for course in obj.courses_to_drop.all()])

    display_courses_to_drop.short_description = 'Courses to Drop'

    def display_courses_to_add(self, obj):
        return ", ".join([course.name for course in obj.courses_to_add.all()])

    display_courses_to_add.short_description = 'Courses to Add'


admin.site.register(CourseCorrectionRequest, CourseCorrectionRequestAdmin)


class GradeReconsiderationRequestAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'reconsideration_text', 'response_text')
    search_fields = ('student__first_name', 'student__last_name', 'course__name')

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return has_user_type_permission(request.user, "DeputyEducational") or has_user_type_permission(request.user,
                                                                                                       "ITManager")


admin.site.register(GradeReconsiderationRequest, GradeReconsiderationRequestAdmin)


class EmergencyDropRequestAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'result', 'student_comment')
    search_fields = ('student__first_name', 'student__last_name', 'course__name')
    list_filter = ('result',)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return has_user_type_permission(request.user, "DeputyEducational") or has_user_type_permission(request.user,
                                                                                                       "ITManager")


admin.site.register(EmergencyDropRequest, EmergencyDropRequestAdmin)


class TermDropRequestAdmin(admin.ModelAdmin):
    list_display = ('student', 'term', 'result', 'student_comment')
    search_fields = ('student__first_name', 'student__last_name', 'term__name')
    list_filter = ('result',)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return has_user_type_permission(request.user, "DeputyEducational") or has_user_type_permission(request.user,
                                                                                                       "ITManager")


admin.site.register(TermDropRequest, TermDropRequestAdmin)
