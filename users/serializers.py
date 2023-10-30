from rest_framework import serializers
from .models import Student
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.contrib.auth.hashers import make_password

from .models import Professor


class StudentSerializer(serializers.ModelSerializer):
    verification_password = serializers.CharField(max_length=255, write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'username', 'password', 'verification_password', 'profile_picture',
                  'mobile', 'national_id'
            , 'gender', 'birth_date', 'entry_year', 'entry_term', 'college', 'study_field'
            , 'military_status', 'seniority', 'average', 'passed_courses', 'current_courses']

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('verification_password'):
            raise serializers.ValidationError({"detail": "passwords does not match"})
        try:
            validate_password(attrs.get('password'))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})
        return super().validate(attrs)

    def create(self, validated_data):
        password = validated_data.pop('password')
        hashed_password = make_password(password)
        validated_data['password'] = hashed_password

        validated_data.pop('verification_password', None)
        return super().create(validated_data)


class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = '__all__'

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = super().create(validated_data)
        if password:
            instance.set_password(password)
            instance.save()

        return instance

    def update(self, instance, validated_data):
        # Remove password from validated_data if it exists
        validated_data.pop('password', None)

        # Update other fields as usual
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
