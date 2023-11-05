from rest_framework import serializers
from courses.models import Faculty


class FacultiesListSerializer(serializers.ModelSerializer):
    class Meta: 
        mode = Faculty
        fields = "__all__"

