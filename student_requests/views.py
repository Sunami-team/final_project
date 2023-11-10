from django.shortcuts import render
from .models import Course, CourseTerm
from .serializers import CourseSerializer, CourseTermSerializer
from users.permissions import IsItManager, IsDeputyEducational, IsStudent
from rest_framework import generics


class CourseListCreate(generics.ListCreateAPIView):
    """
    Course Create and List API View
    """
    serializer_class = CourseSerializer
    permission_classes = [IsItManager, IsDeputyEducational]


class CourseRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    """
    Course Retrieve, Update, Delete API View
    """
    serializer_class = CourseSerializer
    permission_classes = [IsItManager, IsDeputyEducational]


class ClassSchedulesView(generics.RetrieveAPIView):
    """
    Class Schedule Retrieve API View
    """
    queryset = CourseTerm.objects.all()
    serializer_class = CourseTermSerializer
    permission_classes = [IsStudent]
    lookup_field = 'pk'

    def get_queryset(self):
        student_id = self.kwargs.get('pk')

        if student_id == 'me':
            student_id = self.request.user.pk
        
        return CourseTerm.objects.filter(studentcourse__student_id=student_id)


class ExamScheduleView(generics.RetrieveAPIView):
    """
    Exam Schedule Retrieve API View
    """
    queryset = CourseTerm.objects.all()
    serializer_class = CourseTermSerializer
    permission_classes = [IsStudent]
    lookup_field = 'pk'

    def get_queryset(self):
        student_id = self.kwargs.get('pk')

        if student_id == 'me':
            student_id = self.request.user.pk
        
        return CourseTerm.objects.filter(studentcourse__student_id=student_id)
