from .models import Term
from .serializers import TermSerializer

from rest_framework import viewsets, generics


class TermViewSet(viewsets.ModelViewSet):
    queryset = Term.objects.all()
    serializer_class = TermSerializer


class TermDetailAPIView(generics.RetrieveAPIView):
    queryset = Term.objects.all()
    serializer_class = TermSerializer

