from django.db.models import F
from rest_framework import serializers
from .models import Course, Term, StudentCourse, CourseTerm


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["college", "name", "course_unit", "course_type"]


class TermSerializer(serializers.ModelSerializer):
    class Meta:
        model = Term
        fields = "__all__"


class CourseSelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentCourse
        fields = "__all__"


class StudentCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentCourse
        fields = ["student", "grade"]


class TermSerializer(serializers.ModelSerializer):
    students = serializers.SerializerMethodField()
    professors = serializers.SerializerMethodField()

    def get_students(self, obj):
        students = obj.termstudentprofessor_set.all().values(
            first_name=F("students__first_name"), last_name=F("students__last_name")
        )
        return students

    def get_professors(self, obj):
        professors = obj.termstudentprofessor_set.all().values(
            first_name=F("professors__first_name"), last_name=F("professors__last_name")
        )
        return professors

    class Meta:
        model = Term
        fields = [
            "name",
            "start_course_selection",
            "end_course_selection",
            "start_classes",
            "end_classes",
            "start_course_correction",
            "end_course_correction",
            "end_emergency_drop",
            "start_exams",
            "end_term",
            "students",
            "professors",
        ]


class CourseTermSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseTerm
        fields = "__all__"
