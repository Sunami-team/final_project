from django.shortcuts import render
from .models import Student
from .permissions import IsItManager
from rest_framework import viewsets
from .serializers import StudentSerializer
from .pagination import CustomPageNumberPagination
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

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

