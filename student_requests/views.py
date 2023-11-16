from django.shortcuts import render
from rest_framework.views import APIView
from users.models import User, Student
from courses.models import Course, CourseTerm, Term, StudentCourse
from .serializers import CourseSerializer, CourseTermSerializer, TermDropSerializer
from users.permissions import IsItManager, IsDeputyEducational, IsStudent
from rest_framework import generics, status, serializers
from django.shortcuts import get_object_or_404
from users.tasks import send_email
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from courses.models import CourseTerm
from courses.permissions import IsStudent
from users.models import Student, DeputyEducational
from .models import EmergencyDropRequest, TermDropRequest
from .permissions import IsDeputyEducational
from .serializers import EmergencyDropRequestSerializer
from rest_framework.exceptions import NotFound
from .tasks import *

from final_project.student_requests.serializers import EmergencyDropRequestSerializer
from final_project.users.models import DeputyEducational
from final_project.users.permissions import IsDeputyEducational


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
        serializer = self.serializer_class(instance=studnet_term_drop, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        accept = serializer.validated_data['accept']
        deputy_educational_comment = serializer.validated_data['deputy_educational_comment']
        if accept:

            if studnet_term_drop.result == 'Without Seniority':
                student.seniority -= 1
                student.save()
            current_term = studnet_term_drop.term
            # current_term.students.remove(student)
            StudentCourse.objects.filter(student=student, term=current_term).delete()
            try:
                send_email.delay(student.email, f'{student.first_name} {student.last_name} ,Your Term Removed')
                return Response({'result': 'Request Accepted', 'message': deputy_educational_comment},
                                status=status.HTTP_200_OK)
            except:
                raise serializers.ValidationError('Student Email field is Null')
        elif not accept:
            try:
                send_email.delay(student.email,
                                 f'{student.first_name} {student.last_name} ,The request to remove Your Term was not accepted')
                return Response({'result': 'Request Failed', 'message': 'deputy_educational_comment'},
                                status=status.HTTP_200_OK)
            except:
                raise serializers.ValidationError('Student Email field is Null')


class EmergencyDropRequestView(generics.GenericAPIView):
    serializer_class = EmergencyDropRequestSerializer
    permission_classes = [IsAuthenticated, IsStudent]

    def get_queryset(self):
        student_id = self.kwargs.get('pk')
        course_id = self.kwargs.get('c_pk')
        return EmergencyDropRequest.objects.filter(student_id=student_id, course__course_id=course_id)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        student_id = self.kwargs.get('pk')
        course_id = self.kwargs.get('c_pk')
        try:
            student = Student.objects.get(id=student_id)
            course_term = CourseTerm.objects.filter(course_id=course_id).first()
            if not course_term:
                raise CourseTerm.DoesNotExist

            # Check if a request already exists
            existing_request = EmergencyDropRequest.objects.filter(student=student, course=course_term).first()
            if existing_request:
                return Response({"error": "Emergency drop request already exists for this course"},
                                status=status.HTTP_400_BAD_REQUEST)

            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save(student=student, course=course_term)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except (Student.DoesNotExist, CourseTerm.DoesNotExist):
            return Response({"error": "Invalid student or course ID"}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        student_id = self.kwargs.get('pk')
        course_id = self.kwargs.get('c_pk')

        try:
            # Assuming you want to update the first EmergencyDropRequest that matches the criteria
            emergency_drop_request = EmergencyDropRequest.objects.filter(student_id=student_id,
                                                                         course__course_id=course_id).first()
            if not emergency_drop_request:
                return Response({"error": "EmergencyDropRequest not found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = self.get_serializer(emergency_drop_request, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except (Student.DoesNotExist, CourseTerm.DoesNotExist):
            return Response({"error": "Invalid student or course ID"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        student_id = self.kwargs.get('pk')
        course_id = self.kwargs.get('c_pk')

        try:
            # Assuming you want to delete the first EmergencyDropRequest that matches the criteria
            emergency_drop_request = EmergencyDropRequest.objects.filter(student_id=student_id,
                                                                         course__course_id=course_id).first()
            if not emergency_drop_request:
                return Response({"error": "EmergencyDropRequest not found"}, status=status.HTTP_404_NOT_FOUND)

            emergency_drop_request.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except (Student.DoesNotExist, CourseTerm.DoesNotExist):
            return Response({"error": "Invalid student or course ID"}, status=status.HTTP_400_BAD_REQUEST)


class EmergencyDropRequestListView(generics.ListAPIView):
    serializer_class = EmergencyDropRequestSerializer
    permission_classes = [IsAuthenticated, IsDeputyEducational]

    def get_queryset(self):
        user_id = self.kwargs.get('pk')
        User = get_user_model()

        if user_id == 'me':
            user_id = self.request.user.id

        # Check if the user ID corresponds to a DeputyEducational
        try:
            # Try to get a DeputyEducational with the provided ID
            deputy_educational = get_object_or_404(DeputyEducational, pk=user_id)
        except NotFound:
            # If no DeputyEducational found, return an empty queryset
            return EmergencyDropRequest.objects.none()

        # If valid DeputyEducational, return all emergency drop requests
        return EmergencyDropRequest.objects.all()


class EmergencyDropRequestDetailView(generics.RetrieveAPIView):
    serializer_class = EmergencyDropRequestSerializer
    permission_classes = [IsAuthenticated, IsDeputyEducational]

    def get_object(self):
        deputy_id = self.kwargs.get('pk')
        student_id = self.kwargs.get('s_pk')

        # If 'me' is specified, use the current user's ID
        if deputy_id == 'me':
            deputy_id = self.request.user.id

        # Check if the DeputyEducational exists
        try:
            get_object_or_404(DeputyEducational, pk=deputy_id)
        except NotFound:
            # If no DeputyEducational found, raise a NotFound exception
            raise NotFound("DeputyEducational not found.")

        # Filter emergency drop requests based on the student ID
        try:
            emergency_request = get_object_or_404(EmergencyDropRequest, student_id=student_id)
        except NotFound:
            # If no request found for this student, raise a NotFound exception
            raise NotFound("Emergency drop request for the specified student not found.")

        return emergency_request


# The issue in your query is due to incorrect syntax for filtering in Django's QuerySet API. When you want to filter
# based on a field's value, you should use double underscores (__) to access related fields and pass the field value
# as an argument to the filter method, not as a comparison in the method call.
class EmergencyDropRequestApprovalView(generics.UpdateAPIView):
    serializer_class = EmergencyDropRequestSerializer
    permission_classes = [IsAuthenticated, IsDeputyEducational]
    queryset = EmergencyDropRequest.objects.all()
    lookup_url_kwarg = 's_pk'

    def get_object(self):
        deputy_id = self.kwargs.get('pk')
        student_id = self.kwargs.get('s_pk')

        # If 'me' is specified, use the current user's ID
        if deputy_id == 'me':
            deputy_id = self.request.user.id

        # Check if the DeputyEducational exists
        try:
            get_object_or_404(DeputyEducational, pk=deputy_id)
        except NotFound:
            # If no DeputyEducational found, raise a NotFound exception
            raise NotFound("DeputyEducational not found.")

        # Filter emergency drop requests based on the student ID
        try:
            emergency_request = get_object_or_404(EmergencyDropRequest, student_id=student_id)
        except NotFound:
            # If no request found for this student, raise a NotFound exception
            raise NotFound("Emergency drop request for the specified student not found.")

        return emergency_request

    def perform_update(self, serializer):
        emergency_drop_request = serializer.save()
        course_to_drop = emergency_drop_request.course.course
        course_name = emergency_drop_request.course.course.name
        # Sending email based on the result of the request
        if emergency_drop_request.result == 'approved':
            emergency_drop_request.student.current_courses.remove(course_to_drop)

            # Send approval email
            send_approval_email.delay(
                emergency_drop_request.student.email,
                course_name,
            )
            emergency_drop_request.delete()

        elif emergency_drop_request.result == 'rejected':
            # Send rejection email
            send_rejection_email.delay(
                emergency_drop_request.student.email,
                course_name,
                emergency_drop_request.deputy_educational_comment
            )

            emergency_drop_request.delete()
