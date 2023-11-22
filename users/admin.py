from django.contrib import admin
from .models import User, Professor, Student, ITManager, DeputyEducational
from import_export.admin import ImportExportModelAdmin
from import_export import resources

from .permissions import has_user_type_permission


# admin.site.register(User)
# admin.site.register(Professor)
# admin.site.register(Student)
# admin.site.register(ITManager)
# admin.site.register(DeputyEducational)
# Student Resource


class StudentResource(resources.ModelResource):
    class Meta:
        model = Student
        fields = ('id', 'name', 'email', 'department',)
        import_id_fields = ('id',)


# Student Admin
class StudentAdmin(ImportExportModelAdmin):
    resource_class = StudentResource
    list_display = ('username', 'first_name', 'last_name', 'entry_year', 'study_field', 'average')
    search_fields = ('username', 'first_name', 'last_name', 'study_field__name')
    list_filter = ['study_field']

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return has_user_type_permission(request.user, "DeputyEducational") or has_user_type_permission(request.user,
                                                                                                       "ITManager")


admin.site.register(Student, StudentAdmin)


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'user_type')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    list_filter = ('user_type', 'is_staff', 'is_active')

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return has_user_type_permission(request.user, "DeputyEducational") or has_user_type_permission(request.user,
                                                                                                       "ITManager")


admin.site.register(User, UserAdmin)


# Professor Resource
class ProfessorResource(resources.ModelResource):
    class Meta:
        model = Professor
        fields = ('id', 'name', 'email', 'department',)
        import_id_fields = ('id',)


# Professor Admin
class ProfessorAdmin(ImportExportModelAdmin):
    resource_class = ProfessorResource
    list_display = ('username', 'first_name', 'last_name', 'study_field', 'rank')
    search_fields = ('username', 'first_name', 'last_name', 'faculty__name', 'study_field__name')
    list_filter = ['study_field']

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return has_user_type_permission(request.user, "DeputyEducational") or has_user_type_permission(request.user,
                                                                                                       "ITManager")


admin.site.register(Professor, ProfessorAdmin)


class ITManagerAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name')
    search_fields = ('username', 'first_name', 'last_name')

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return has_user_type_permission(request.user, "DeputyEducational") or has_user_type_permission(request.user,
                                                                                                       "ITManager")


admin.site.register(ITManager, ITManagerAdmin)


class DeputyEducationalAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name',  'study_field')
    search_fields = ('username', 'first_name', 'last_name', 'faculty__name', 'study_field__name')
    list_filter = ['study_field']

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return has_user_type_permission(request.user, "DeputyEducational") or has_user_type_permission(request.user,
                                                                                                       "ITManager")


admin.site.register(DeputyEducational, DeputyEducationalAdmin)
