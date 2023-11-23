from users.models import User, Student, Professor, DeputyEducational
from courses.models import Course, CourseTerm, Term, StudentCourse
from .serializers import TermDropSerializer, AssistantGradeReconsiderationRequestSerializer, \
    CorrectionRequestSerializer, CorrectionShowSerializer, EmergencyDropRequestSerializer, \
    MilitaryServiceRequestSerializer, MilitaryServiceRequestRetriveSerializer, TermRemovalRequestSerializer, \
    StudentGradeReconsiderationRequestSerializer, ClassScheduleSerializer, ExamScheduleSerializer, \
    StudentSelectionFormSerializer
from users.permissions import IsItManager, IsDeputyEducational, IsProfessor, IsStudent, IsItManagerOrDeputyEducational
from rest_framework import generics, status, serializers, viewsets, permissions
from .serializers import TermDropSerializer, AssistantGradeReconsiderationRequestSerializer, \
    CorrectionRequestSerializer, CorrectionShowSerializer, EmergencyDropRequestSerializer, \
    MilitaryServiceRequestSerializer, MilitaryServiceRequestRetriveSerializer, CourseCorrectionRequestSerializer, \
    MilitaryServiceRequestApprovalSerializer
from .serializers import TermDropSerializer, SelectionRequestSerializer, \
    SelectionShowSerializer
from users.permissions import IsItManager, IsDeputyEducational, IsStudent
from rest_framework import generics, status, serializers
from django.shortcuts import get_object_or_404
from users.tasks import send_email
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from .models import *
from .permissions import IsDeputyEducational, IsStudent
from rest_framework.exceptions import NotFound
from .tasks import send_approval_email, send_rejection_email, create_and_send_pdf
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from rest_framework.views import APIView
from users.pagination import CustomPageNumberPagination
from django.utils.translation import gettext as _
from rest_framework.viewsets import ModelViewSet
from . import serializers


class ClassScheduleViewSet(viewsets.ViewSet):
    """
    The Class Schedule API View
    """
    serializer_class = ClassScheduleSerializer

    def list(self, request, student_id=None):
        student_id = request.user.id
        student_courses = StudentCourse.objects.filter(student_id=student_id)
        serializer = ClassScheduleSerializer(student_courses, many=True)
        return Response(serializer.data)


class ExamScheduleViewSet(viewsets.ViewSet):
    """
    The Exam Schedule API View
    """
    serializer_class = ExamScheduleSerializer

    def list(self, request, student_id=None):
        student_id = request.user.id
        student_courses = StudentCourse.objects.filter(student_id=student_id)
        serializer = ExamScheduleSerializer(student_courses, many=True)
        return Response(serializer.data)


# Assistant Access Remove Term

class AssistantRemoveTermList(generics.ListAPIView):
    queryset = TermDropRequest.objects.all()
    serializer_class = TermDropSerializer
    permission_classes = [IsDeputyEducational]


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
            return Response({ـ('error'): 'درخواست حذف ترم مورد نظر یافت نشد.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TermRemovalRequestSerializer(term_removal_request, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        try:
            term_removal_request = TermDropRequest.objects.get(pk=pk)
        except TermDropRequest.DoesNotExist:
            return Response({_('error'): 'درخواست حذف ترم مورد نظر یافت نشد.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TermRemovalRequestSerializer(term_removal_request)
        return Response(serializer.data)

    def destroy(self, request, pk):
        try:
            term_removal_request = TermDropRequest.objects.get(pk=pk)
        except TermDropRequest.DoesNotExist:
            return Response({_('error'): 'درخواست حذف ترم مورد نظر یافت نشد.'}, status=status.HTTP_404_NOT_FOUND)

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
            raise serializers.ValidationError(_('Student Does Not Exist'))

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
                raise serializers.ValidationError(_('Student Email field is Null'))
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


######################
# GRADE RECONSIDERTION
# /assistant/{pk,me}/courses/{c-pk}/prof-approved/ GET
class AssistantGradeReconsiderationRequestList(APIView):
    permission_classes = [IsDeputyEducational]

    def get(self, request, professor_id, course_id):
        try:
            all_requets = GradeReconsiderationRequest.objects.filter(course=course_id, course__professor=professor_id)
            serializer = AssistantGradeReconsiderationRequestSerializer(all_requets, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except GradeReconsiderationRequest.DoesNotExist:
            return Response({_('errors'): _('Request Does not exist')}, status=status.HTTP_404_NOT_FOUND)


class AssistantGradeReconsiderationRequestStudentDetail(generics.GenericAPIView):
    permission_classes = [IsDeputyEducational]
    serializer_class = AssistantGradeReconsiderationRequestSerializer

    def get(self, request, professor_id, course_id, student_id):
        try:
            request_detail = GradeReconsiderationRequest.objects.get(course=course_id, course__professor=professor_id,
                                                                     student=student_id)
            serializer = AssistantGradeReconsiderationRequestSerializer(request_detail)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except GradeReconsiderationRequest.DoesNotExist:
            return Response({_('errors'): _('Request Does not exist')}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, professor_id, course_id, student_id):
        request_detail = GradeReconsiderationRequest.objects.get(course=course_id, course__professor=professor_id,
                                                                 student=student_id)
        serializer = AssistantGradeReconsiderationRequestSerializer(instance=request_detail, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if serializer.validated_data['approve']:
            try:
                course_term = CourseTerm.objects.get(id=course_id)
                student_course = StudentCourse.objects.get(student=student_id, course_term=course_id,
                                                           term=course_term.term)
                student_course.course_status = 'pass'
                student_course.save()
            except StudentCourse.DoesNotExist:
                return Response({_('details'): _('Studet Course Does Not exist')}, status=status.HTTP_200_OK)
        else:
            return Response({_('details'): _('Request Failed')}, status=status.HTTP_200_OK)
        return Response({_('details'): _('Request Accepted')}, status=status.HTTP_200_OK)


# Course Studet Correction

# /student/{pk/me}/course-substitution/create/
class CreateCorrectionRequestByStudent(generics.GenericAPIView):
    queryset = CourseCorrectionStudentRequest.objects.all()
    serializer_class = CorrectionRequestSerializer
    permission_classes = [IsStudent]
    pagination_class = CustomPageNumberPagination

    def get(self, request, pk):
        studnet = Student.objects.get(id=pk)
        return Response({_('studnet'): f'{studnet.first_name} {studnet.last_name}', _('details'): _('add or remove')},
                        status=status.HTTP_200_OK)

    def post(self, request, pk):
        student = Student.objects.get(pk=pk)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['student'] = student
        for course_to_add in serializer.validated_data['courses_to_add']:
            if course_to_add in serializer.validated_data['courses_to_drop']:
                return Response({_('detail'): _('You can not add and drop a course in same time !')},
                                status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({_('detail'): _('Pre Request Created')}, status=status.HTTP_201_CREATED)

    # /student/{pk/me}/course-substitution/


class DetailCorrectionRequestByStudent(APIView):
    permission_classes = [IsStudent]
    pagination_class = CustomPageNumberPagination

    def get(self, request, pk):
        correction_requests = CourseCorrectionStudentRequest.objects.filter(student__id=pk)
        serializer = CorrectionShowSerializer(correction_requests, many=True)
        studnet = Student.objects.get(pk=pk)
        return Response({_('student'): f'{studnet.first_name} {studnet.last_name}', _('details'): serializer.data},
                        status=status.HTTP_200_OK)


# /student/{pk/me}/course-substitution/check/
class CorrectionShowErrors(APIView):
    permission_classes = [IsStudent]

    def get(self, request, pk, term_id):
        add_errors = {}
        drop_errors = {}
        student = Student.objects.get(id=pk)
        current_term = Term.objects.get(id=term_id)
        all_current_courses = StudentCourse.objects.filter(student=student, term=current_term)
        all_passed_courses = StudentCourse.objects.filter(student=student).exclude(id__in=all_current_courses)
        correction_student = CourseCorrectionStudentRequest.objects.get(student=student)

        # تعداد واحد های حذف یا اضافه از ۶ بیشتر نباشد
        sum_of_unit_add = 0
        for correction in correction_student.courses_to_add.all():
            sum_of_unit_add += correction.course.course_unit

        if sum_of_unit_add > 6:
            add_errors['total'] = ['added courses most be less than 6']

        sum_of_unit_remove = 0
        for correction in correction_student.courses_to_drop.all():
            sum_of_unit_remove += correction.course.course_unit

        if sum_of_unit_remove > 6:
            drop_errors['total'] = ['added courses most be less than 6']

        # ADD
        for add_course in correction_student.courses_to_add.all():
            add_errors[add_course.course.name] = []

            # درس پیشنیاز حتما باید در وضعیت قبول باشد
            for pre_requisite in add_course.course.courses_required.all():
                if pre_requisite not in all_passed_courses:
                    add_errors[add_course.course.name].append(f"You Did not passed {pre_requisite.name}")

            # درس تکراری یا پاس شده نباید برداشت
            if add_course.course in all_passed_courses:
                add_errors[add_course.course.name].append('You Passed This Course')

            # تکمیل بودن ظرفیت کلاس
            if add_course.capacity == StudentCourse.objects.filter(course_term=add_course.course).count():
                add_errors[add_course.course.name].append('Course is Full')

            # تداخل زمانی کلاس و امتحان
            for current_course in all_current_courses:
                if add_course.class_time == current_course.course_term.class_time:
                    add_errors[add_course.course.name].append('Course Interference time')
                if add_course.exam_date_time == current_course.course_term.exam_date_time:
                    add_errors[add_course.course.name].append('Exam Interference time')

            # رشته تحصیلی اشتباه
            # if add_course.course.study_field != student.study_field:
            #     add_errors[add_course.course.name].append('Wrong Study field')

        # DROP
        for drop_course in correction_student.courses_to_drop.all():
            drop_errors[drop_course.course.name] = []
            # نمی توان درسی که هم نیاز دارد را حذف کرد
            for studnet_course in all_current_courses:
                if studnet_course.course != drop_course.course:
                    for co_requisite in studnet_course.course_term.course.co_requisites.all():
                        if co_requisite == drop_course:
                            drop_errors[drop_course.course.name].append('this Course have Co Requisite')

        if not all(add_errors.values()) and not all(drop_errors.values()):
            correction_student.approval_status = True
            correction_student.save()

        return Response({_('add_errors'): add_errors, _('drop_errors'): drop_errors,
                         _('status'): correction_student.approval_status}, status=status.HTTP_200_OK)


# /student/{pk/me}/course-substitution/submit/
class CorrectionSubmit(APIView):
    permission_classes = [IsStudent]

    @transaction.atomic
    def post(self, request, pk):
        try:
            with transaction.atomic():

                student = Student.objects.get(id=pk)
                correction_student = CourseCorrectionStudentRequest.objects.get(student=student)
                if correction_student.approval_status:
                    final_correction = CourseCorrectionStudentSendToAssistant.objects.create(
                        student=correction_student.student,
                    )
                    correction_student = CourseCorrectionStudentRequest.objects.get(student=student)
                    for add_courses in correction_student.courses_to_add.all():
                        final_correction.courses_to_add.add(add_courses)
                    for drop_courses in correction_student.courses_to_drop.all():
                        final_correction.courses_to_drop.add(drop_courses)
                    return Response(_('add to Correction Submit'), status=status.HTTP_200_OK)
                else:
                    raise serializers.ValidationError(_('Add and drop Corses does not correct'))
        except Exception as e:
            return Response(_('We Have errors'), status=status.HTTP_200_OK)


# /student/{pk/me}/course-substitution/send-form/{term_id}
class CorrectionSendForm(APIView):
    def get(self, request, pk, term_id):
        student = Student.objects.get(id=pk)
        correction_student = CourseCorrectionStudentSendToAssistant.objects.get(student=student)
        try:
            selected_term = Term.objects.get(id=term_id)
        except Term.DoesNotExist:
            return Response(_('Term Does NOT exist'), status=status.HTTP_404_NOT_FOUND)
        for add_course in correction_student.courses_to_add.all():
            StudentCourse.objects.create(
                student=student,
                course_term=add_course.course,
                term=selected_term
            )
        if not correction_student.courses_to_add.all():
            return Response(_('Corses Corrections is Empty'), status=status.HTTP_400_BAD_REQUEST)
        return Response(_('Corses Corrections DONE'), status=status.HTTP_200_OK)


class MilitaryServiceRequestViewSet(ModelViewSet):

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return MilitaryServiceRequestRetriveSerializer
        else:
            return MilitaryServiceRequestSerializer

    permission_classes = [IsAuthenticated, IsStudent]

    def perform_create(self, serializer):
        student_instance = Student.objects.get(pk=self.request.user.id)
        serializer.save(student=student_instance)

    lookup_field = 'student_id'

    def get_queryset(self):
        student_id = self.kwargs['student_id']
        return MilitaryServiceRequest.objects.filter(student_id=student_id)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['student_id'] = self.kwargs['student_id']
        return context


class GradeReconsiderationRequestViewSet(ModelViewSet):
    queryset = GradeReconsiderationRequest.objects.all()

    permission_classes = [IsAuthenticated, IsProfessor]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.GradeReconsiderationRequestRetriveSerializer
        elif self.request.method == 'POST':
            return serializers.GradeReconsiderationResponseSerializer

    def get_queryset(self):
        professor_id = self.kwargs.get('professor_id')
        course_id = self.kwargs.get('course_id')
        queryset = super().get_queryset()
        return queryset.filter(course_id=course_id, course__professor_id=professor_id)

    def retrieve(self, request, *args, **kwargs):
        student_id = self.kwargs.get('student_id')
        queryset = self.get_queryset()
        instance = queryset.get(student_id=student_id)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class CreateSelectionRequestByStudent(generics.GenericAPIView):
    queryset = CourseSelectionStudentRequest.objects.all()
    serializer_class = SelectionRequestSerializer
    permission_classes = [IsStudent]
    pagination_class = CustomPageNumberPagination

    def get(self, request, pk):
        studnet = Student.objects.get(id=pk)
        return Response({'studnet': f'{studnet.first_name} {studnet.last_name}', 'details': 'add or remove'},
                        status=status.HTTP_200_OK)

    def post(self, request, pk):
        student = Student.objects.get(pk=pk)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['student'] = student
        for course_to_add in serializer.validated_data['courses_to_add']:
            if course_to_add in serializer.validated_data['courses_to_drop']:
                return Response({'detail': 'You can not add and drop a course in same time !'},
                                status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({'detail': 'Pre Request Created'}, status=status.HTTP_201_CREATED)


class DetailSelectionRequestByStudent(APIView):
    permission_classes = [IsStudent]
    pagination_class = CustomPageNumberPagination

    def get(self, request, pk):
        selection_requests = CourseSelectionStudentRequest.objects.filter(student__id=pk)
        serializer = SelectionShowSerializer(selection_requests, many=True)
        studnet = Student.objects.get(pk=pk)
        return Response({'student': f'{studnet.first_name} {studnet.last_name}', 'details': serializer.data},
                        status=status.HTTP_200_OK)


class SelectionShowErrors(APIView):
    permission_classes = [IsStudent]

    def get(self, request, pk, term_id):
        add_errors = {}
        drop_errors = {}
        student = Student.objects.get(id=pk)
        current_term = Term.objects.get(id=term_id)
        all_current_courses = StudentCourse.objects.filter(student=student, term=current_term)
        all_passed_courses = StudentCourse.objects.filter(student=student).exclude(id__in=all_current_courses)
        selection_student = CourseSelectionStudentRequest.objects.get(student=student)

        # تعداد واحد های حذف یا اضافه از 20 بیشتر نباشد
        sum_of_unit_add = 0
        for selection in selection_student.courses_to_add.all():
            sum_of_unit_add += selection.course.course_unit
        for selection in selection_student.courses_to_drop.all():
            sum_of_unit_add -= selection.course.course_unit
        if current_term.pre_GPA_term >= 17:
            if sum_of_unit_add > 24:
                add_errors['total'] = ['added courses most be less than 24']
        else:
            if sum_of_unit_add > 20:
                add_errors['total'] = ['added courses most be less than 20']

        if sum_of_unit_add < 12:
            add_errors['total'] = ['added courses most be upper than 12']

        # ADD
        for add_course in selection_student.courses_to_add.all():
            add_errors[add_course.course.name] = []

            # درس پیشنیاز حتما باید در وضعیت قبول باشد
            for pre_requisite in add_course.course.courses_required.all():
                if pre_requisite not in all_passed_courses:
                    add_errors[add_course.course.name].append(f"You Did not passed {pre_requisite.name}")

            # درس تکراری یا پاس شده نباید برداشت
            if add_course.course in all_passed_courses:
                add_errors[add_course.course.name].append('You Passed This Course')

            # تکمیل بودن ظرفیت کلاس
            if add_course.capacity == StudentCourse.objects.filter(course_term=add_course.course).count():
                add_errors[add_course.course.name].append('Course is Full')

            # تداخل زمانی کلاس و امتحان
            for current_course in all_current_courses:
                if add_course.class_time == current_course.course_term.class_time:
                    add_errors[add_course.course.name].append('Course Interference time')
                if add_course.exam_date_time == current_course.course_term.exam_date_time:
                    add_errors[add_course.course.name].append('Exam Interference time')

        # DROP
        for drop_course in selection_student.courses_to_drop.all():
            drop_errors[drop_course.course.name] = []
            # نمی توان درسی که هم نیاز دارد را حذف کرد
            for studnet_course in all_current_courses:
                if studnet_course.course != drop_course.course:
                    for co_requisite in studnet_course.course_term.course.co_requisites.all():
                        if co_requisite == drop_course:
                            drop_errors[drop_course.course.name].append('this Course have Co Requisite')

        print(add_errors.values())
        print(drop_errors.values())
        if not all(add_errors.values()) and not all(drop_errors.values()):
            selection_student.approval_status = True
            selection_student.save()

        return Response(
            {'add_errors': add_errors, 'drop_errors': drop_errors, 'status': selection_student.approval_status},
            status=status.HTTP_200_OK)


class SelectionSubmit(APIView):
    permission_classes = [IsStudent]

    @transaction.atomic
    def post(self, request, pk):
        try:
            with transaction.atomic():

                student = Student.objects.get(id=pk)
                selection_student = CourseSelectionStudentRequest.objects.get(student=student)
                if selection_student.approval_status:
                    final_selection = CourseSelectionStudentSendToAssistant.objects.create(
                        student=selection_student.student,
                    )
                    selection_student = CourseSelectionStudentRequest.objects.get(student=student)
                    for add_courses in selection_student.courses_to_add.all():
                        final_selection.courses_to_add.add(add_courses)
                    for drop_courses in selection_student.courses_to_drop.all():
                        final_selection.courses_to_drop.add(drop_courses)
                    return Response('add to Selection Submit', status=status.HTTP_200_OK)
                else:
                    raise serializers.ValidationError('Add and drop Corses does not correct')
        except Exception as e:
            return Response('We Have errors', status=status.HTTP_200_OK)


class SelectionSendForm(APIView):
    def get(self, request, pk, term_id):
        student = Student.objects.get(id=pk)
        selection_student = CourseSelectionStudentSendToAssistant.objects.get(student=student)
        try:
            selected_term = Term.objects.get(id=term_id)
        except Term.DoesNotExist:
            return Response('Term Does NOT exist', status=status.HTTP_404_NOT_FOUND)
        for add_course in selection_student.courses_to_add.all():
            StudentCourse.objects.create(
                student=student,
                course_term=add_course.course,
                term=selected_term
            )
        if not selection_student.courses_to_add.all():
            return Response('Corses Selections is Empty', status=status.HTTP_400_BAD_REQUEST)
        return Response('Corses Selections DONE', status=status.HTTP_200_OK)


class GradeReconsiderationRequestView(generics.GenericAPIView):
    queryset = GradeReconsiderationRequest.objects.all()
    serializer_class = StudentGradeReconsiderationRequestSerializer
    permission_classes = [IsStudent]
    pagination_class = CustomPageNumberPagination

    def get(self, request, course_id, student_id):
        # student = Student.objects.get(id=student_id)
        try:
            data = GradeReconsiderationRequest.objects.get(course__course=course_id, student=student_id)
            serializer = self.serializer_class(data)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except GradeReconsiderationRequest.DoesNotExist:
            return Response(_("Request Does Not Exists!"), status=status.HTTP_404_NOT_FOUND)

    def post(self, request, course_id, student_id):
        data = GradeReconsiderationRequest.objects.filter(course__course=course_id, student=student_id).exists()
        if not data:
            try:
                student_course = StudentCourse.objects.get(student=student_id, course_term=course_id)
            except StudentCourse.DoesNotExist:
                return Response(_("Object Does Not Exists!"), status=status.HTTP_404_NOT_FOUND)
            grade = student_course.grade
            if grade:
                serializer = self.serializer_class(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response({_("details"): _("request created successfully")}, status=status.HTTP_201_CREATED)
            else:
                return Response(_("Grade Does Not Exists!"), status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(_("Your request is filled!!"), status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, course_id, student_id):
        try:
            data = GradeReconsiderationRequest.objects.get(course__course=course_id, student=student_id)
            serializer = self.serializer_class(instance=data, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({_("details"): _("request modified successfully")}, status=status.HTTP_200_OK)
        except GradeReconsiderationRequest.DoesNotExist:
            return Response(_("Request Does Not Exists!"), status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, course_id, student_id):

        try:
            data = GradeReconsiderationRequest.objects.get(course__course=course_id, student=student_id)
            data.delete()
            return Response(_("Removed Successfully"), status=status.HTTP_200_OK)
        except GradeReconsiderationRequest.DoesNotExist:
            return Response(_("Request Does Not Exists!"), status=status.HTTP_404_NOT_FOUND)


class StudentRequestList(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsDeputyEducational]
    serializer_class = MilitaryServiceRequestApprovalSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('pk_or_me')
        User = get_user_model()

        if user_id == 'me':
            user_id = self.request.user.id

        # Check if the user ID corresponds to a DeputyEducational
        try:
            # Try to get a DeputyEducational with the provided ID
            deputy_educational = get_object_or_404(DeputyEducational, pk=user_id)
        except NotFound:
            # If no DeputyEducational found, return an empty queryset
            return MilitaryServiceRequest.objects.none()

        # If valid DeputyEducational, return all emergency drop requests
        return MilitaryServiceRequest.objects.all()


class StudentRequestDetail(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsDeputyEducational]
    serializer_class = MilitaryServiceRequestApprovalSerializer

    def get_object(self):
        deputy_id = self.kwargs.get('pk_or_me')
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
            request = get_object_or_404(MilitaryServiceRequest, student_id=student_id)
        except NotFound:
            # If no request found for this student, raise a NotFound exception
            raise NotFound("request for the specified student not found.")
        return request


class StudentSelectionForm(generics.GenericAPIView):
    queryset = CourseRegistrationRequest.objects.all()
    permission_classes = [IsProfessor]
    serializer_class = StudentSelectionFormSerializer
    pagination_class = CustomPageNumberPagination

    def get(self, request, professor_id):
        try:
            requests = CourseRegistrationRequest.objects.filter(adviser_professor=professor_id)
            serializer = StudentSelectionFormSerializer(requests, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CourseRegistrationRequest.DoesNotExist:
            return Response({_('errors'): _('courses selected does not exist')}, status=status.HTTP_404_NOT_FOUND)


class MilitaryServiceRequestApproval(generics.UpdateAPIView):
    serializer_class = MilitaryServiceRequestApprovalSerializer
    permission_classes = [IsDeputyEducational]
    queryset = MilitaryServiceRequest.objects.all()

    def get_queryset(self):
        deputy_id = self.kwargs.get('d_pk')
        student_id = self.kwargs.get('pk')
        student = Student.objects.get(id=student_id)
        queryset = super().get_queryset()
        return queryset.filter(student=student)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        new_status = serializer.validated_data.get('status')
        email = instance.student.email
        text = ""

        if new_status == True:  # Assuming True indicates approval and False indicates rejection
            text = f"Dear {instance.student.full_name}, Your request was approved."
        else:
            text = f"Dear {instance.student.full_name}, Your request was rejected."
        create_and_send_pdf.delay(email, text)

        return Response(serializer.data)


class StudentSelectionFormDetailAndApproveRejection(generics.GenericAPIView):
    queryset = CourseRegistrationRequest.objects.all()
    permission_classes = [IsProfessor]
    serializer_class = StudentSelectionFormSerializer
    pagination_class = CustomPageNumberPagination

    def get(self, request, professor_id, student_id, term_id):
        try:
            request_detail = CourseRegistrationRequest.objects.get(adviser_professor=professor_id, student=student_id)
            serializer = self.serializer_class(request_detail)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CourseRegistrationRequest.DoesNotExist:
            return Response({_('errors'): _('Student and supervisor Do Not Match')}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, professor_id, term_id, student_id, ):
        request_detail = CourseRegistrationRequest.objects.get(adviser_professor=professor_id, student=student_id)
        serializer = self.serializer_class(instance=request_detail, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        student = Student.objects.get(id=student_id)
        if serializer.validated_data['approve']:
            request_detail.approval_status = True
            request_detail.save()
            courses_selected = request_detail.requested_courses.all()
            send_email.delay(student.email, f'{student.first_name} {student.last_name} ,Registration Approved!')
            term = Term.objects.get(id=term_id)
            for courseterm in courses_selected:
                StudentCourse.objects.create(student=student, course_term=courseterm.course,
                                             real_course_term=courseterm, term=term)
        else:
            send_email.delay(student.email, f'{student.first_name} {student.last_name} ,Registration Not Approved!')
            return Response({_('details'): _('Request Failed')}, status=status.HTTP_200_OK)
        return Response({_('details'): _('Request Accepted')}, status=status.HTTP_200_OK)


class CourseCorrectionRequestView(ModelViewSet):
    queryset = CourseCorrectionRequest.objects.all()
    serializer_class = CourseCorrectionRequestSerializer

    def list(self, request, pk=None):
        course_correction_requests = CourseCorrectionRequest.objects.filter(student__professor=pk)
        serializer = self.get_serializer(course_correction_requests, many=True)
        return Response(serializer.data)
 
    def retrieve(self, request, pk=None, s_pk=None):
        course_correction_form = get_object_or_404(CourseCorrectionStudentSendToAssistant, student__professor=pk, pk=s_pk)
        serializer = self.get_serializer(course_correction_form)
        return Response(serializer.data)