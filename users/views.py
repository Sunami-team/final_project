from django.shortcuts import render
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, ListAPIView

from .models import Student, Professor
from .permissions import IsItManager
from rest_framework import viewsets
from .serializers import StudentSerializer, ProfessorSerializer
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
    filterset_fields = {'first_name': ['exact', 'in'], 'last_name': ['exact', 'in'], 'national_id': ['exact'],
                        'college': ['exact'],
                        'study_field': ['exact'], 'entry_year': ['exact'], 'military_status': ['exact'],
                        'personal_number': ['exact']}
    search_fields = ['first_name', 'last_name']
    ordering_fields = ['id', 'last_name']


class ProfessorListView(ListAPIView):
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


# @method_decorator(csrf_exempt,  name='dispatch')
class ProfessorCreateView(CreateAPIView):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    permission_classes = [IsItManager]


class ProfessorRetrieveView(RetrieveAPIView):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    permission_classes = [IsItManager]


class ProfessorUpdateView(UpdateAPIView):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    permission_classes = [IsItManager]


class ProfessorDeleteView(DestroyAPIView):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    permission_classes = [IsItManager]
