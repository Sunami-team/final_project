from django.shortcuts import render
from .permissions import IsItManager
from rest_framework import viewsets
from .serializers import LoginSerializer, ChangePasswordSerializer, StudentSerializer, ProfessorSerializer, AssistanSerializer
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, ListAPIView, GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .permissions import IsItManager
from rest_framework import viewsets
from .serializers import LoginSerializer, ChangePasswordSerializer, StudentSerializer, ProfessorSerializer, AssistanSerializer, FacultiesListSerializer
from rest_framework import generics
from django.contrib.auth import authenticate, login, logout
from .models import User, ChangePasswordToken, Student, DeputyEducational, Professor
from rest_framework import generics, status, viewsets
from django.contrib.auth import authenticate, login, logout
from .models import User, ChangePasswordToken, Student, DeputyEducational
from rest_framework import generics
from .serializers import LoginSerializer, ChangePasswordSerializer, StudentSerializer, AssistanSerializer
from rest_framework import generics, status, viewsets
# from rest_framework.generics import UpdateAPIView
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
import random
from django.shortcuts import render
from .pagination import CustomPageNumberPagination
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from courses.models import Faculty
from rest_framework.mixins import CreateModelMixin, ListModelMixin
#from rest_framework.permissions import IsAuthenticatedOrReadOnly


class AssistanList(generics.ListAPIView):
    """
    Assistant List API View
    """
    queryset = DeputyEducational.objects.all()
    serializer_class = AssistanSerializer


class AssistanDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Assistant Detail API View
    """
    queryset = DeputyEducational.objects.all()
    serializer_class = AssistanSerializer


class AssistanCreate(generics.CreateAPIView):
    """
    Assistant Create API View
    """
    queryset = DeputyEducational.objects.all()
    serializer_class = AssistanSerializer


class AssistanUpdate(generics.UpdateAPIView):
    """
    Assistant Update API View
    """
    queryset = DeputyEducational.objects.all()
    serializer_class = AssistanSerializer


class AssistanDelete(generics.DestroyAPIView):
    """
    Assistant Delete API View
    """
    queryset = DeputyEducational.objects.all()
    serializer_class = AssistanSerializer


class LoginApiView(generics.GenericAPIView):
    """
    This API is for login using GenericAPIView
    """
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
    """
    This API is for logout using GenericAPIView
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        Token.objects.get(user=request.user).delete()
        return Response({"message": "You have been successfully logged out."}, status=status.HTTP_200_OK)


class ChangePasswordRequestApiView(generics.GenericAPIView):
    """
    This API is for change password request using GenericAPIView
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        user = request.user
        token = random.randint(1000, 10000)
        ChangePasswordToken.objects.create(user=user, token=token)

        return Response({'token': token, 'detail': 'Token generated successfully'}, status=status.HTTP_200_OK)


class ChangePasswordActionApiView(generics.UpdateAPIView):
    """
    This API is for change password action using GenericAPIView
    """
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


class StudentViewset(viewsets.ModelViewSet):
    """
    This viewset is for Create, List, Retrieve, Updtate, Delete  --> Student
    """
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    permission_classes = [IsItManager]
    pagination_class = CustomPageNumberPagination

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = {'first_name': ['exact', 'in'], 'last_name': ['exact', 'in'], 'national_id': ['exact'],
                        'college': ['exact'],
                        'study_field': ['exact'], 'entry_year': ['exact'], 'military_status': ['exact'],
                        'personal_number': ['exact']}
    search_fields = ['first_name', 'last_name']
    ordering_fields = ['id', 'last_name']


class ProfessorListView(generics.ListAPIView):
    """
    Professor List API View
    """
    queryset = Professor.objects.all().order_by('id')
    serializer_class = ProfessorSerializer
    permission_classes = [IsItManager]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        # page_size = self.request.query_params.get('page_size', 10)

        first_name = self.request.query_params.get('first_name', None)
        last_name = self.request.query_params.get('last_name', None)
        professor_id = self.request.query_params.get('professor_id', None)
        national_id = self.request.query_params.get('national_id', None)
        faculty = self.request.query_params.get('faculty', None)
        study_field = self.request.query_params.get('study_field', None)
        rank = self.request.query_params.get('rank', None)

        if first_name:
            queryset = queryset.filter(user__first_name__icontains=first_name)
        if last_name:
            queryset = queryset.filter(user__last_name__icontains=last_name)
        if professor_id:
            queryset = queryset.filter(id=professor_id)
        if national_id:
            queryset = queryset.filter(user__national_id=national_id)
        if faculty:
            queryset = queryset.filter(faculty__name=faculty)
        if study_field:
            queryset = queryset.filter(study_field__name=study_field)
        if rank:
            queryset = queryset.filter(rank=rank)
        return queryset


class ProfessorCreateView(generics.CreateAPIView):
    """
    Professor Create API View
    """
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    permission_classes = [IsItManager]


class ProfessorRetrieveView(generics.RetrieveAPIView):
    """
    Professor Retrieve API View
    """
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    permission_classes = [IsItManager]


class ProfessorUpdateView(generics.UpdateAPIView):
    """
    Professor Update API View
    """
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    permission_classes = [IsItManager]


class ProfessorDeleteView(generics.DestroyAPIView):
    """
    Professor Delete API View
    """
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    permission_classes = [IsItManager]
    ordering_fields = ['id', 'last_name']
    
  
class FacultiesListCreate(ListCreateAPIView):
    queryset = Faculty.objects.all()
    serializer_class = FacultiesListSerializer
    permission_class = [IsItManager]
    # pagination_class = DefaultPagination


class FacultiesInformation(RetrieveUpdateDestroyAPIView):
    queryset = Faculty.objects.all()
    serializer_class = FacultiesListSerializer
