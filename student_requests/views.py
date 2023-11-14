from django.shortcuts import render
from users.models import User, Student, Professor
from courses.models import Course, CourseTerm, Term, StudentCourse
from .serializers import CourseSerializer, CourseTermSerializer, TermDropSerializer, AssistantGradeReconsiderationRequestSerializer
from users.permissions import IsItManager, IsDeputyEducational, IsStudent
from rest_framework import generics, status, serializers
from django.shortcuts import get_object_or_404
from users.tasks import send_email
from .models import TermDropRequest, GradeReconsiderationRequest
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

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
from rest_framework import viewsets, permissions, status

from .models import TermDropRequest
from .serializers import TermRemovalRequestSerializer
from rest_framework.response import Response


class TermRemovalRequestViewSet(viewsets.ModelViewSet):
    queryset = TermDropRequest.objects.all()
    serializer_class = TermRemovalRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        serializer = TermRemovalRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        try:
            term_removal_request = TermDropRequest.objects.get(pk=pk)
        except TermDropRequest.DoesNotExist:
            return Response({'error': 'درخواست حذف ترم مورد نظر یافت نشد.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TermRemovalRequestSerializer(term_removal_request, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        try:
            term_removal_request = TermDropRequest.objects.get(pk=pk)
        except TermDropRequest.DoesNotExist:
            return Response({'error': 'درخواست حذف ترم مورد نظر یافت نشد.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TermRemovalRequestSerializer(term_removal_request)
        return Response(serializer.data)

    def destroy(self, request, pk):
        try:
            term_removal_request = TermDropRequest.objects.get(pk=pk)
        except TermDropRequest.DoesNotExist:
            return Response({'error': 'درخواست حذف ترم مورد نظر یافت نشد.'}, status=status.HTTP_404_NOT_FOUND)

        term_removal_request.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
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

######################
# GRADE RECONSIDERTION
# /assistant/{pk,me}/courses/{c-pk}/prof-approved/ GET
class AssistantGradeReconsiderationRequestList(APIView): 
    permission_classes = [IsDeputyEducational]
    def get(self, request , professor_id, course_id):
        try:
            all_requets = GradeReconsiderationRequest.objects.filter(course=course_id, course__professor=professor_id)
            serializer = AssistantGradeReconsiderationRequestSerializer(all_requets, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except GradeReconsiderationRequest.DoesNotExist:
            return Response({'errors':'Request Does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
class AssistantGradeReconsiderationRequestStudentDetail(generics.GenericAPIView):
    permission_classes = [IsDeputyEducational]
    serializer_class = AssistantGradeReconsiderationRequestSerializer
    def get(self, request , professor_id, course_id, student_id):
        try:
            requet_detail = GradeReconsiderationRequest.objects.get(course=course_id, course__professor=professor_id, student=student_id)
            serializer = AssistantGradeReconsiderationRequestSerializer(requet_detail)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except GradeReconsiderationRequest.DoesNotExist:
            return Response({'errors':'Request Does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request , professor_id, course_id, student_id):
        requet_detail = GradeReconsiderationRequest.objects.get(course=course_id, course__professor=professor_id, student=student_id)
        serializer = AssistantGradeReconsiderationRequestSerializer(instance=requet_detail, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if serializer.validated_data['approve']:
            try:
                course_term = CourseTerm.objects.get(id=course_id)
                student_course = StudentCourse.objects.get(student=student_id, course_term=course_id, term=course_term.term)
                student_course.course_status = 'pass'
                student_course.save()
            except StudentCourse.DoesNotExist:
                return Response({'details': 'Studet Course Does Not exist'}, status=status.HTTP_200_OK)
        else:
            return Response({'details': 'Request Failed'}, status=status.HTTP_200_OK)   
        return Response({'details': 'Request Accepted'}, status=status.HTTP_200_OK)
