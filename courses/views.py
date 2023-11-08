from rest_framework import viewsets
from rest_framework.generics import RetrieveAPIView

from courses.models import Term
from courses.serializers import TermSerializer

from rest_framework import generics
from .serializers import CourseSelectionSerializer


class TermViewSet(viewsets.ModelViewSet):
    queryset = Term.objects.all()
    serializer_class = TermSerializer


class TermDetailAPIView(RetrieveAPIView):
    queryset = Term.objects.all()
    serializer_class = TermSerializer


class CourseSelectionCreateView(generics.CreateAPIView):
    serializer_class = CourseSelectionSerializer


    def create(self, request, *args, **kwargs):
        # بررسی زمان شروع و پایان انتخاب واحد
        # بررسی تعداد واحدهای حداکثر و حداقل
        # بررسی شرایط پیش‌نیازی
        # بررسی وضعیت دروس
        # ثبت انتخاب واحد
        return super().create(request, *args, **kwargs)
