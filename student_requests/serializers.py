from .models import Course, CourseTerm
from rest_framework import serializers


class CourseSerializer(serializers.ModelSerilaizer):
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