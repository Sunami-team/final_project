from django.contrib import admin
from .models import Faculty, StudyField, Course, Term, CourseTerm, StudentCourse
# Register your models here.

admin.site.register(Faculty)
admin.site.register(StudyField)
admin.site.register(Course)
admin.site.register(Term)
admin.site.register(CourseTerm)
admin.site.register(StudentCourse)