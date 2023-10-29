from django.contrib.auth import authenticate, login, logout
from rest_framework import serializers
from .models import User, ChangePasswordToken


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