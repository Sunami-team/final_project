from rest_framework import serializers

from users.models import DeputyEducational


class AssistanSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeputyEducational
        field = '__all__'