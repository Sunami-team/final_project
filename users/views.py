from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.views import ObtainAuthToken
from .models import User, ChangePasswordToken
from .serializers import LoginSerializer, ChangePasswordSerializer
from rest_framework import generics, status
from rest_framework.generics import UpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
import random


class LoginApiView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        login(request, user)

        token, created = Token.objects.get_or_create(user=user)
        response_data = {
                'token': token.key,
                'user': user.username
            }
        return Response(response_data, status=status.HTTP_200_OK)


class LogoutApiView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        Token.objects.get(user=request.user).delete()
        return Response({"message": "You have been successfully logged out."}, status=status.HTTP_200_OK)


class ChangePasswordRequestApiView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        user = request.user
        token = random.randint(1000, 10000)
        ChangePasswordToken.objects.create(user=user, token=token)

        return Response({'token': token, 'detail': 'Token generated successfully'}, status=status.HTTP_200_OK)


class ChangePasswordActionApiView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        user = self.request.user
        token = self.request.data['token']
        return ChangePasswordToken.objects.get(user=user, token=token)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        new_password = request.data['new_password']
        
        user = instance.user
        user.set_password(new_password)
        user.save()

        instance.delete()
        
        return Response({'detail': 'Password changed successfully'}, status=status.HTTP_200_OK)