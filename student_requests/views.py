from django.shortcuts import render
from users.models import User, Student
from courses.models import Course, CourseTerm, Term, StudentCourse
from .serializers import CourseSerializer, CourseTermSerializer, TermDropSerializer
from users.permissions import IsItManager, IsDeputyEducational, IsStudent
from rest_framework import generics, status, serializers
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .models import TermDropRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from users.tasks import send_email
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


class ClassSchedulesView(generics.ListAPIView):
    """
    Class Schedule List API View
    """
    serializer_class = CourseTermSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        param = self.kwargs.get('pk')

        if param and param.isdigit():
            professor = get_object_or_404(User, pk=param, user_type='professor')
            return CourseTerm.objects.filter(professor=professor)

        elif param == 'me':
            return CourseTerm.objects.filter(course__in=user.current_courses.all())
        
        return CourseTerm.objects.none()
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        serialized_data = self.serializer_class(queryset, many=True, context={'request': request}).data
        custom_response = [
            {
                'course': item['course'],
                'class_day': item['class_day'],
                'class_time': item['class_time'],
                'class_location': item['class_location'],
            }
            for item in serialized_data
        ]
        return self.get_paginated_response(custom_response)


class ExamSchedulesView(generics.ListAPIView):
    """
    Exam Schedule List API View
    """
    serializer_class = CourseTermSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        param = self.kwargs.get('pk')

        if param and param.isdigit():
            professor = get_object_or_404(User, pk=param, user_type='professor')
            return CourseTerm.objects.filter(professor=professor)

        elif param == 'me':
            return CourseTerm.objects.filter(course__in=user.current_courses.all())
        
        return CourseTerm.objects.none()
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        serialized_data = self.serializer_class(queryset, many=True, context={'request': request}).data
        custom_response = [
            {
                'course': item['course'],
                'exam_date_time': item['exam_date_time'],
                'exam_location': item['exam_location'],
            }
            for item in serialized_data
        ]
        return self.get_paginated_response(custom_response)


# Assistant Access Remove Term

class AssistantRemoveTermList(generics.ListAPIView):
    queryset = TermDropRequest.objects.all()
    serializer_class = TermDropSerializer
    permission_classes = [IsDeputyEducational]

class AssistantRemoveTermStudentDetail(APIView):
    queryset = TermDropRequest.objects.all()
    serializer_class = TermDropSerializer
    permission_classes = [IsDeputyEducational]

    def get(self, request, term_id, student_id):
        try:
            student = Student.objects.get(id=student_id)
            term = Term.objects.get(id=term_id)
            remove_term = TermDropRequest.objects.get(student=student, term=term)
            serializer = self.serializer_class(remove_term)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            raise serializers.ValidationError('Student Does Not Exist')

    def put(self, request, term_id, student_id):
        student = Student.objects.get(id=student_id)
        current_term = Term.objects.get(id=term_id)
        studnet_term_drop = TermDropRequest.objects.get(student=student, term=current_term)
        serializer = self.serializer_class(instance=studnet_term_drop ,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        accept = serializer.validated_data['accept']
        deputy_educational_comment = serializer.validated_data['deputy_educational_comment']
        if accept :

            if studnet_term_drop.result == 'Without Seniority':
                student.seniority -= 1
                student.save()
            current_term = studnet_term_drop.term
            # current_term.students.remove(student)
            StudentCourse.objects.filter(student=student, term=current_term).delete()
            try:
                send_email.delay(student.email, f'{student.first_name} {student.last_name} ,Your Term Removed')
                return Response({'result':'Request Accepted', 'message': deputy_educational_comment}, status=status.HTTP_200_OK)
            except:
                raise serializers.ValidationError('Student Email field is Null')
        elif not accept:
            try:
                send_email.delay(student.email, f'{student.first_name} {student.last_name} ,The request to remove Your Term was not accepted')
                return Response({'result':'Request Failed', 'message': 'deputy_educational_comment'}, status=status.HTTP_200_OK)
            except:
                raise serializers.ValidationError('Student Email field is Null')
