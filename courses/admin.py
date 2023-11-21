from django.contrib import admin
from .models import *


admin.site.register(
    (
        Faculty,
        Course,
        CourseRequistes,
        Term,
        CourseTerm,
        StudentCourse,
        TermStudentProfessor,
        StudyField,
    )
)
