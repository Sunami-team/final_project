from courses.models import Course, CourseTerm
from rest_framework import serializers
from .models import TermDropRequest

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['name', 'faculty', 'pre_requisites', 'co_requisites', 'course_unit', 'course_type']


class CourseTermSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseTerm
        fields = [
            'course',
            'course_day',
            'course_time'
            'class_location',
            'exam_date_time',
            'exam_location'
        ]

class TermDropSerializer(serializers.ModelSerializer):
    student_first_name = serializers.CharField(source='student.first_name', read_only=True)
    student_last_name = serializers.CharField(source='student.last_name', read_only=True)
    student_id = serializers.CharField(source='student.id', read_only=True)
    term_name = serializers.CharField(source='term.name', read_only=True)
    accept = serializers.BooleanField(default=False, write_only=True)
    class Meta:
        model = TermDropRequest
        fields = ('student_id', 'student_first_name', 'student_last_name', 'term_name', 'result', 'student_comment', 'deputy_educational_comment', 'accept')
        read_only_fields = ('student_id', 'student_first_name', 'student_last_name', 'term_name', 'result', 'student_comment')