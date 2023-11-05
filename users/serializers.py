from django.contrib.auth import authenticate, login, logout
from rest_framework import serializers
from .models import User, ChangePasswordToken, DeputyEducational
from rest_framework import serializers
from users.models import Student
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.contrib.auth.hashers import make_password


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']
    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if user:
                data['user'] = user
            else:
                raise serializers.ValidationError("Invalid credentials")
        else:
            raise serializers.ValidationError("Username and Password are required.")
        return data


class ChangePasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(write_only=True)
    class Meta:
        model = ChangePasswordToken
        fields = ['id', 'user', 'token', 'created_at', 'new_password']


class StudentSerializer(serializers.ModelSerializer):
    verification_password = serializers.CharField(max_length=255, write_only=True)
    password = serializers.CharField(write_only=True)
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'username', 'password', 'verification_password', 'profile_picture','mobile', 'national_id'
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


class AssistanSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeputyEducational
        field = '__all__'