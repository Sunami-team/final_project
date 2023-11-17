from courses.models import Course, CourseTerm
from rest_framework import serializers
from .models import TermDropRequest, GradeReconsiderationRequest, CourseSelectionStudentRequest

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['name', 'faculty', 'pre_requisites', 'co_requisites', 'course_unit', 'course_type']
from rest_framework import serializers

from student_requests.models import TermDropRequest


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

class TermRemovalRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermDropRequest
        fields = '__all__'


class SelectionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSelectionStudentRequest
        exclude = ['student', 'approval_status']

class CourseTermSerializerForSelection(serializers.ModelSerializer):
    course_id = serializers.CharField(source='course.id')
    course_name = serializers.CharField(source='course.name')
    class Meta:
        model = CourseTerm
        fields = ['course_id', 'course_name']


class SelectionShowSerializer(serializers.ModelSerializer):
    student_first_name = serializers.CharField(source='student.first_name')
    student_last_name = serializers.CharField(source='student.last_name')
    class Meta:
        model = CourseSelectionStudentRequest
        fields = ['student_first_name', 'student_last_name', 'courses_to_add', 'courses_to_drop']

    def to_representation(self, instance):
        request = self.context.get('request')
        rep = super().to_representation(instance)
        rep['courses_to_add'] = CourseTermSerializerForSelection(instance.courses_to_add, context={'request':request}, many=True).data
        rep['courses_to_drop'] = CourseTermSerializerForSelection(instance.courses_to_drop, context={'request':request}, many=True).data

        return rep