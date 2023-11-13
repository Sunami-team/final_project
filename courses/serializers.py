from rest_framework import serializers
from courses.models import Term, StudentCourse


class TermSerializer(serializers.ModelSerializer):
    class Meta:
        model = Term
        fields = '__all__'


class CourseSelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentCourse
        fields = '__all__'


class StudentCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentCourse
        fields = ['student', 'grade']