from courses.models import Course, CourseTerm
from rest_framework import serializers
from .models import TermDropRequest, GradeReconsiderationRequest, CourseCorrectionStudentRequest, EmergencyDropRequest, MilitaryServiceRequest
from django.conf import settings
import os


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
        fields = ('student_id', 'student_first_name', 'student_last_name', 'term_name', 'result', 'student_comment',
                  'deputy_educational_comment', 'accept')
        read_only_fields = (
            'student_id', 'student_first_name', 'student_last_name', 'term_name', 'result', 'student_comment')


class TermRemovalRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermDropRequest
        fields = '__all__'


class EmergencyDropRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyDropRequest
        fields = '__all__'


class AssistantGradeReconsiderationRequestSerializer(serializers.ModelSerializer):
    student_first_name = serializers.CharField(source='student.first_name', read_only=True)
    student_last_name = serializers.CharField(source='student.last_name', read_only=True)
    course_name = serializers.CharField(source='course.course.name', read_only=True)
    professor_first_name = serializers.CharField(source='course.professor.first_name', read_only=True)
    professor_last_name = serializers.CharField(source='course.professor.last_name', read_only=True)
    approve = serializers.BooleanField(write_only=True)

    class Meta:
        model = GradeReconsiderationRequest
        fields = ('student_first_name', 'student_last_name', 'course_name', 'reconsideration_text', 'response_text',
                  'professor_first_name', 'professor_last_name', 'approve')
        read_only_fields = ('student_first_name', 'student_last_name', 'course_name', 'reconsideration_text',)


class CorrectionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCorrectionStudentRequest
        exclude = ['student', 'approval_status']


class CourseTermSerializerForCorrection(serializers.ModelSerializer):
    course_id = serializers.CharField(source='course.id')
    course_name = serializers.CharField(source='course.name')

    class Meta:
        model = CourseTerm
        fields = ['course_id', 'course_name']


class CorrectionShowSerializer(serializers.ModelSerializer):
    student_first_name = serializers.CharField(source='student.first_name')
    student_last_name = serializers.CharField(source='student.last_name')

    class Meta:
        model = CourseCorrectionStudentRequest
        fields = ['student_first_name', 'student_last_name', 'courses_to_add', 'courses_to_drop']

    def to_representation(self, instance):
        request = self.context.get('request')
        rep = super().to_representation(instance)
        rep['courses_to_add'] = CourseTermSerializerForCorrection(instance.courses_to_add, context={'request': request},
                                                                  many=True).data
        rep['courses_to_drop'] = CourseTermSerializerForCorrection(instance.courses_to_drop,
                                                                   context={'request': request}, many=True).data

        return rep


class MilitaryServiceRequestSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        self.student_id = kwargs.pop('student_id', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = MilitaryServiceRequest
        fields = ['term', 'proof_document', 'issuance_place']

    def create(self, validated_data):
        proof_document = self.context['request'].data.get('proof_document')

        file_path = os.path.join('military_docs', proof_document.name)
        with open(os.path.join(settings.MEDIA_ROOT, file_path), 'wb') as file:
            file.write(proof_document.read())

        military_service_request = MilitaryServiceRequest.objects.create(
            student=validated_data['student'],
            term=validated_data['term'],
            proof_document=proof_document,
            issuance_place=validated_data['issuance_place']
        )

        return military_service_request


class MilitaryServiceRequestRetriveSerializer(serializers.ModelSerializer):
    student = serializers.CharField()
    term = serializers.CharField()

    class Meta:
        model = MilitaryServiceRequest
        fields = ['student', 'term', 'proof_document', 'issuance_place']
        read_only_fields = ['proof_document']



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

class GradeReconsiderationRequestRetriveSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField()
    course = serializers.StringRelatedField()

    class Meta:
        model = GradeReconsiderationRequest
        fields = ['student', 'course', 'reconsideration_text']
        read_only_fields = ['student', 'course', 'reconsideration_text']


class GradeReconsiderationResponseSerializer(serializers.ModelSerializer):
    approve = serializers.BooleanField(write_only=True)
    class Meta:
        model = GradeReconsiderationRequest
        fields = ['student', 'course', 'response_text', 'approve']

        
class StudentGradeReconsiderationRequestSerializer(serializers.ModelSerializer):
    # student_first_name = serializers.CharField(source='student.first_name')
    # student_last_name = serializers.CharField(source='student.last_name')
    class Meta: 
        model = GradeReconsiderationRequest
        fields = ('student','course', 'reconsideration_text', 'response_text', 'approve')
        read_only_fields = ("response_text",)
