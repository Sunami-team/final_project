from django.contrib.auth import authenticate, login, logout
from .models import User, ChangePasswordToken, DeputyEducational
from rest_framework import serializers
from .models import Student
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.contrib.auth.hashers import make_password
from .models import Professor
from django.contrib.auth import get_user_model


User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    user_type = serializers.ChoiceField(choices=User.USER_TYPE_CHOICES)  # Add the user_type field

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'user_type']  # Include the user_type field

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data.get('email', ''),  # Optional field
            user_type=validated_data['user_type'],  # Set the user_type
        )
        user.set_password(validated_data['password'])
        
        # You can add logic here to handle user-specific fields based on user_type
        if user.user_type == 'student':
            user.student_id = validated_data.get('student_id')
        elif user.user_type == 'professor':
            user.employee_id = validated_data.get('employee_id')
        elif user.user_type == 'it_manager':
            user.it_manager_id = validated_data.get('it_manager_id')
        elif user.user_type == 'deputy_educational':
            user.deputy_id = validated_data.get('deputy_id')
        
        user.save()
        return user


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


class AssistanSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeputyEducational
        field = '__all__'
