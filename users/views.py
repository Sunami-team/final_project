from rest_framework import generics

from users.models import DeputyEducational
from users.serializers import AssistanSerializer


class AssistanList(generics.ListAPIView):
    queryset = DeputyEducational.objects.all()
    serializer_class = AssistanSerializer


class AssistanDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DeputyEducational.objects.all()
    serializer_class = AssistanSerializer


class AssistanCreate(generics.CreateAPIView):
    queryset = DeputyEducational.objects.all()
    serializer_class = AssistanSerializer


class AssistanUpdate(generics.UpdateAPIView):
    queryset = DeputyEducational.objects.all()
    serializer_class = AssistanSerializer


class AssistanDelete(generics.DestroyAPIView):
    queryset = DeputyEducational.objects.all()
    serializer_class = AssistanSerializer
