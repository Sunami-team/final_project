from rest_framework import viewsets
from rest_framework.generics import RetrieveAPIView

from courses.models import Term, StudentCourse
from courses.serializers import TermSerializer

from rest_framework import generics
from .serializers import CourseSelectionSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action


class TermViewSet(viewsets.ModelViewSet):
    queryset = Term.objects.all()
    serializer_class = TermSerializer


class TermDetailAPIView(RetrieveAPIView):
    queryset = Term.objects.all()
    serializer_class = TermSerializer


class StudentViewSet(viewsets.ModelViewSet):
    @action(detail=True, methods=['post'])
    def create_course_selection(self, request, pk=None):
        student = self.get_object()
        serializer = CourseSelectionSerializer(data=request.data)
        # بررسی زمان شروع و پایان انتخاب واحد
        # بررسی تعداد واحدهای حداکثر و حداقل
        # بررسی شرایط پیش‌نیازی
        # بررسی وضعیت دروس
        # ثبت انتخاب واحد
        if serializer.is_valid():
            course_selection = serializer.save(student=student)
            return Response(CourseSelectionSerializer(course_selection).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def course_selection(self, request, pk=None):
        student = self.get_object()
        course_selection = StudentCourse.objects.filter(student=student).first()

        if course_selection:
            serializer = CourseSelectionSerializer(course_selection)
            return Response(serializer.data)
        return Response({'message': 'دانشجو هنوز فرم انتخاب واحد ایجاد نکرده است.'}, status=status.HTTP_404_NOT_FOUND)
