from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from courses.models import Faculty
from users.serializers import FacultiesListSerializer
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .permissions import IsItManager
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from users.serializers import FacultiesListSerializer

class FacultiesListCreate(ListCreateAPIView):
    queryset = Faculty.objects.all()
    serializer_class = FacultiesListSerializer
    permission_class = [IsItManager]
    # pagination_class = DefaultPagination


class FacultiesInformation(RetrieveUpdateDestroyAPIView):
    queryset = Faculty.objects.all()
    serializer_class = FacultiesListSerializer
