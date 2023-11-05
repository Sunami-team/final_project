from rest_framework import serializers
from .models import CorrectionTemporaryRequests, TermDropRequest
from users.models import Student

class CorrectionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CorrectionTemporaryRequests
        exclude = ['student']

    def get_select_course_name(self, obj):
        return obj.select_course.name if obj.select_course else None


class CorrectionShowSerializer(serializers.ModelSerializer):
    select_course_name = serializers.SerializerMethodField()
    class Meta:
        model = CorrectionTemporaryRequests
        fields = ['select_course', 'add_or_remove', 'select_course_name']

    def get_select_course_name(self, obj):
        
        return obj.select_course.course.name if obj.select_course else None
    
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