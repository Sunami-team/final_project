from .models import Student, Professor
from .permissions import IsItManager, IsStudentOrDeputyEducational, IsDeputyEducational, IsProfessorOrDeputyEducational
from rest_framework import viewsets
from .serializers import StudentSerializer, DeputyEducationalStudentSerializer, DeputyEducationalProfessorSerializer
from .pagination import CustomPageNumberPagination
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics

class StudentViewset(viewsets.ModelViewSet):
    """
    This viewset is for Create, List, Retrieve, Updtate, Delete  --> Student
    """
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    permission_classes = [IsItManager]
    pagination_class = CustomPageNumberPagination

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = {'first_name':['exact', 'in'], 'last_name':['exact', 'in'], 'national_id':['exact'], 'college':['exact'],
                        'study_field':['exact'], 'entry_year':['exact'], 'military_status':['exact'], 'personal_number':['exact']}
    search_fields = ['first_name', 'last_name']
    ordering_fields = ['id', 'last_name']



class EducationalDeputyStudentsList(generics.ListAPIView):
    """
    Deputy Educational Access to students List
    """
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    pagination_class = CustomPageNumberPagination
    permission_classes = [IsDeputyEducational]


    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = {'first_name':['exact', 'in'], 'last_name':['exact', 'in'], 'national_id':['exact'], 'college':['exact'],
                        'study_field':['exact'], 'entry_year':['exact'], 'military_status':['exact'], 'personal_number':['exact']}
    search_fields = ['first_name', 'last_name']
    ordering_fields = ['id', 'last_name']


class EducationalDeputyStudentDetail(generics.RetrieveUpdateAPIView):
    """
    Deputy Educational Access to a student Data Detail
    """
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    permission_classes = [IsStudentOrDeputyEducational]



class EducationalDeputyProfessorsList(generics.ListAPIView):
    serializer_class = DeputyEducationalProfessorSerializer
    queryset = Professor.objects.all()
    pagination_class = CustomPageNumberPagination
    permission_classes = [IsDeputyEducational]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['first_name', 'last_name', 'personal_number', 'national_id', 'faculty',
                        'study_field', 'expertise', 'rank']
    search_fields = ['first_name', 'last_name']
    ordering_fields = ['id', 'last_name']


class EducationalDeputyProfessorDetail(generics.RetrieveAPIView):
    serializer_class = DeputyEducationalProfessorSerializer
    queryset = Professor.objects.all()
    permission_classes = [IsProfessorOrDeputyEducational]
