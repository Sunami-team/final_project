from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

from courses.models import Term
from courses.serializers import TermSerializer


class TermViewSet(viewsets.ModelViewSet):
    queryset = Term.objects.all()
    serializer_class = TermSerializer