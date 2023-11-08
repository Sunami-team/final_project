from rest_framework import serializers

from student_requests.models import TermDropRequest


class TermRemovalRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermDropRequest
        fields = '__all__'