from django.shortcuts import render
from users.models import User, Student, Professor
from courses.models import Course, CourseTerm, Term, StudentCourse
from .serializers import CourseSerializer, CourseTermSerializer, TermDropSerializer, AssistantGradeReconsiderationRequestSerializer, CorrectionRequestSerializer, CorrectionShowSerializer
from users.permissions import IsItManager, IsDeputyEducational, IsStudent
from rest_framework import generics, status, serializers
from django.shortcuts import get_object_or_404
from users.tasks import send_email
from .models import TermDropRequest, GradeReconsiderationRequest, CourseCorrectionStudentSendToAssistant, CourseCorrectionStudentRequest
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from rest_framework.views import APIView
from users.pagination import CustomPageNumberPagination
from django.utils.translation import gettext as _

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
                return Response({_('result'):_('Request Accepted'), _('message'): deputy_educational_comment}, status=status.HTTP_200_OK)
            except:
                raise serializers.ValidationError(_('Student Email field is Null'))
        elif not accept:
            try:
                send_email.delay(student.email, f'{student.first_name} {student.last_name} ,The request to remove Your Term was not accepted')
                return Response({_('result'):_('Request Failed'), _('message'): _('deputy_educational_comment')}, status=status.HTTP_200_OK)
            except:
                raise serializers.ValidationError(_('Student Email field is Null'))

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
            return Response({_('errors'):_('Request Does not exist')}, status=status.HTTP_404_NOT_FOUND)
    
class AssistantGradeReconsiderationRequestStudentDetail(generics.GenericAPIView):
    permission_classes = [IsDeputyEducational]
    serializer_class = AssistantGradeReconsiderationRequestSerializer
    def get(self, request , professor_id, course_id, student_id):
        try:
            requet_detail = GradeReconsiderationRequest.objects.get(course=course_id, course__professor=professor_id, student=student_id)
            serializer = AssistantGradeReconsiderationRequestSerializer(requet_detail)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except GradeReconsiderationRequest.DoesNotExist:
            return Response({_('errors'):_('Request Does not exist')}, status=status.HTTP_404_NOT_FOUND)
        
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
        return Response({_('studnet'): f'{studnet.first_name} {studnet.last_name}',_('details'): _('add or remove')}, status=status.HTTP_200_OK)
    
    def post(self, request, pk):
        student = Student.objects.get(pk=pk)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['student'] = student
        for course_to_add in serializer.validated_data['courses_to_add']:
            if course_to_add in serializer.validated_data['courses_to_drop']:
                return Response({_('detail'): _('You can not add and drop a course in same time !')}, status=status.HTTP_400_BAD_REQUEST)

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
        return Response({_('student'):f'{studnet.first_name} {studnet.last_name}', _('details'):serializer.data}, status=status.HTTP_200_OK)
    
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


        return Response({_('add_errors'):add_errors, _('drop_errors'):drop_errors, _('status'):correction_student.approval_status}, status=status.HTTP_200_OK)


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