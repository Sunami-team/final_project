from rest_framework import viewsets
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, OR

from .models import Term
from .serializers import *
from rest_framework import generics
from .serializers import CourseSelectionSerializer
from django.db.models import Sum
from django.utils import timezone
from .models import Term, StudentCourse, CourseTerm
from .serializers import (
    CourseSelectionSerializer,
    TermSerializer,
    StudentCourseSerializer,
    CourseTermSerializer,
)
from django.db.models import Sum
from django.utils import timezone
from .models import Term, StudentCourse
from .serializers import CourseSelectionSerializer, TermSerializer, StudentCourseSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, generics
import pandas as pd
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from users.permissions import IsProfessor, IsStudent
from rest_framework.viewsets import ModelViewSet
from users.permissions import (
    IsItManager,
    IsDeputyEducational,
    IsItManagerOrDeputyEducational,
)
from .permissions import IsItManager, IsAdminOrEducationalDeputyOrAdvisor
from django.utils.translation import gettext as _
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from users.pagination import CustomPageNumberPagination
from datetime import datetime
from users.models import DeputyEducational, Student
from django.shortcuts import get_object_or_404


class CourseListCreate(generics.ListCreateAPIView):
    """
    Course Create and List API View
    """

    serializer_class = CourseSerializer
    permission_classes = [IsItManagerOrDeputyEducational]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == "it_manager":
            return Course.objects.all()

        elif user.user_type == "deputy_educational":
            deputy_educational = get_object_or_404(DeputyEducational, pk=user.pk)
            return Course.objects.filter(college=deputy_educational.college)

        else:
            return Course.objects.none()


class CourseRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    """
    Course Retrieve, Update, Delete API View
    """

    serializer_class = CourseSerializer
    permission_classes = [IsItManagerOrDeputyEducational]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == "it_manager":
            return Course.objects.all()

        elif user.user_type == "deputy_educational":
            deputy_educational = get_object_or_404(DeputyEducational, pk=user.pk)
            return Course.objects.filter(college=deputy_educational.college)

        else:
            return Course.objects.none()


class TermViewSet(viewsets.ModelViewSet):
    queryset = Term.objects.all()
    serializer_class = TermSerializer


class TermDetailAPIView(generics.RetrieveAPIView):
    queryset = Term.objects.all()
    serializer_class = TermSerializer


class StudentViewSet(viewsets.ModelViewSet):
    @action(detail=True, methods=['post'])
    def create_course_selection(self, request, pk=None):
        student = self.get_object()
        serializer = CourseSelectionSerializer(data=request.data)

        # بررسی زمان شروع و پایان انتخاب واحد
        term_name = request.data.get('term_name', 0)
        term = Term.objects.get(name=term_name)  # ترم جاری را بر اساس منطق برنامه شما باید انتخاب کنید
        if not (term.start_course_selection <= timezone.now() <= term.end_course_selection):
            return Response({'error': 'زمان انتخاب واحد به پایان رسیده است.'}, status=status.HTTP_400_BAD_REQUEST)

        # بررسی تعداد واحدهای حداکثر و حداقل
        min_credit_units = 12  # حداقل تعداد واحدهای مجاز
        max_credit_units = 20  # حداکثر تعداد واحدهای مجاز
        selected_units = request.data.get('units', 0)
        if not (min_credit_units <= selected_units <= max_credit_units):
            return Response({'error': 'تعداد واحدهای انتخاب شده نامعتبر است.'}, status=status.HTTP_400_BAD_REQUEST)

        # بررسی شرایط پیش‌نیازی
        prerequisites = request.data.get('prerequisites', [])
        for prerequisite_id in prerequisites:
            if not student.passed_courses.filter(id=prerequisite_id).exists():
                return Response({'error': 'شما شرایط پیش‌نیاز را برآورده نکرده‌اید.'},
                                status=status.HTTP_400_BAD_REQUEST)

        # بررسی وضعیت دروس
        ongoing_courses = student.current_courses.filter(term=term)
        if len(ongoing_courses) > 0:
            return Response({'error': 'شما قبلاً دروسی را در این ترم انتخاب کرده‌اید.'},
                            status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            # ثبت انتخاب واحد
            course_selection = serializer.save(student=student)

            # احتساب واحدها
            student_units = student.current_courses.filter(term=term).aggregate(Sum('course_unit'))[
                'course_unit__sum']
            if student_units is None:
                student_units = 0
            student_units += selected_units
            if student_units > max_credit_units:
                # اگر تعداد واحدهای دانشجو بیشتر از حداکثر مجاز است، انتخاب واحد لغو می‌شود
                course_selection.delete()
                return Response({'error': 'تعداد واحدهای انتخاب شده بیشتر از حداکثر مجاز است.'},
                                status=status.HTTP_400_BAD_REQUEST)

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


class CourseSelectionViewSet(viewsets.ViewSet):
    # POST /student/{pk/me}/course-selection/check/

    @action(detail=True, methods=['post'])
    def check(self, request, pk=None):
        pass

    # POST /student/{pk/me}/course-selection/submit/
    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        pass

    # POST /student/{pk/me}/course-selection/send-form/
    @action(detail=True, methods=['post'])
    def send_form(self, request, pk=None):
        pass


class CourseSelectionCreateView(generics.CreateAPIView):
    serializer_class = CourseSelectionSerializer

    def create(self, request, *args, **kwargs):
        # بررسی زمان شروع و پایان انتخاب واحد
        # بررسی تعداد واحدهای حداکثر و حداقل
        # بررسی شرایط پیش‌نیازی
        # بررسی وضعیت دروس
        # ثبت انتخاب واحد
        return super().create(request, *args, **kwargs)


class TermViewSet(ModelViewSet):
    serializer_class = TermSerializer
    queryset = Term.objects.all().prefetch_related(
        'termstudentprofessor_set__students', 'termstudentprofessor_set__professors')
    permission_classes = [IsItManager]


class TermDetailAPIView(generics.RetrieveAPIView):
    queryset = Term.objects.all()
    serializer_class = TermSerializer


class StudentViewSet(viewsets.ModelViewSet):
    @action(detail=True, methods=['post'])
    def create_course_selection(self, request, pk=None):
        student = self.get_object()
        serializer = CourseSelectionSerializer(data=request.data)

        # بررسی زمان شروع و پایان انتخاب واحد
        term_name = request.data.get('term_name', 0)
        term = Term.objects.get(name=term_name)  # ترم جاری را بر اساس منطق برنامه شما باید انتخاب کنید
        if not (term.start_course_selection <= timezone.now() <= term.end_course_selection):
            return Response({'error': 'زمان انتخاب واحد به پایان رسیده است.'}, status=status.HTTP_400_BAD_REQUEST)

        # بررسی تعداد واحدهای حداکثر و حداقل
        min_credit_units = 12  # حداقل تعداد واحدهای مجاز
        max_credit_units = 20  # حداکثر تعداد واحدهای مجاز
        selected_units = request.data.get('units', 0)
        if not (min_credit_units <= selected_units <= max_credit_units):
            return Response({'error': 'تعداد واحدهای انتخاب شده نامعتبر است.'}, status=status.HTTP_400_BAD_REQUEST)

        # بررسی شرایط پیش‌نیازی
        prerequisites = request.data.get('prerequisites', [])
        for prerequisite_id in prerequisites:
            if not student.passed_courses.filter(id=prerequisite_id).exists():
                return Response({'error': 'شما شرایط پیش‌نیاز را برآورده نکرده‌اید.'},
                                status=status.HTTP_400_BAD_REQUEST)

        # بررسی وضعیت دروس
        ongoing_courses = student.current_courses.filter(term=term)
        if len(ongoing_courses) > 0:
            return Response({'error': 'شما قبلاً دروسی را در این ترم انتخاب کرده‌اید.'},
                            status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            # ثبت انتخاب واحد
            course_selection = serializer.save(student=student)

            # احتساب واحدها
            student_units = student.current_courses.filter(term=term).aggregate(Sum('course_unit'))[
                'course_unit__sum']
            if student_units is None:
                student_units = 0
            student_units += selected_units
            if student_units > max_credit_units:
                # اگر تعداد واحدهای دانشجو بیشتر از حداکثر مجاز است، انتخاب واحد لغو می‌شود
                course_selection.delete()
                return Response({'error': 'تعداد واحدهای انتخاب شده بیشتر از حداکثر مجاز است.'},
                                status=status.HTTP_400_BAD_REQUEST)

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


class CourseSelectionViewSet(viewsets.ViewSet):
    # POST /student/{pk/me}/course-selection/check/

    @action(detail=True, methods=['post'])
    def check(self, request, pk=None):
        pass

    # POST /student/{pk/me}/course-selection/submit/
    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        pass

    # POST /student/{pk/me}/course-selection/send-form/
    @action(detail=True, methods=['post'])
    def send_form(self, request, pk=None):
        pass


class CourseSelectionCreateView(generics.CreateAPIView):
    serializer_class = CourseSelectionSerializer

    def create(self, request, *args, **kwargs):
        # بررسی زمان شروع و پایان انتخاب واحد
        # بررسی تعداد واحدهای حداکثر و حداقل
        # بررسی شرایط پیش‌نیازی
        # بررسی وضعیت دروس
        # ثبت انتخاب واحد
        return super().create(request, *args, **kwargs)


class PostScoresApiView(APIView):
    def post(self, request, pk, c_pk):
        # Assuming that the uploaded file is in the 'file' field of the request
        file = request.FILES.get('file')

        if not file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Read the Excel file into a DataFrame
            df = pd.read_excel(file)

            # Get the course term using the provided professor and course IDs
            course_term = CourseTerm.objects.get(professor=pk, course=c_pk)

            # Loop through the rows in the DataFrame and update the grades
            for index, row in df.iterrows():
                personal_number = row['student']
                grade = row['grade']

                # Assuming you have a proper way to match students by name
                student = StudentCourse.objects.get(student__personal_number=personal_number, real_course_term=course_term)

                # Update the grade for the student
                student.grade = grade
                student.save()

            return Response({"message": "Grades updated successfully"}, status=status.HTTP_200_OK)

        except Exception as e:

            return Response({_("error"): str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class CourseTermList(generics.GenericAPIView):
     serializer_class = CourseTermSerializer
     queryset = CourseTerm.objects.all()
     permission_classes = permission_classes = [IsItManager, IsDeputyEducational]
     filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
     filterset_fields = {'term': ['exact', 'in'], 'course': ['exact', 'in']}
     search_fields = ['term', 'course']
     ordering_fields = ['id', 'term']
     def get(self, request, term_id):
        try:
            data = CourseTerm.objects.all()
            serializer = CourseTermSerializer(data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CourseTerm.DoesNotExist:
            return Response("Course Does Not Exists!", status=status.HTTP_404_NOT_FOUND)


     def post(self, request, term_id):
        term = Term.objects.get(id=term_id)
        start_term_selection = term.start_course_selection
        end_course_correction = term.end_course_correction
        current_date = datetime.now().date()
        print(current_date)
        print(start_term_selection)
        print(end_course_correction)

        if current_date < end_course_correction and current_date > start_term_selection:
            serializer = CourseTermSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"details": "Course Term Created!"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"details": "Time is Up!!!"}, status=status.HTTP_400_BAD_REQUEST)



class CourseTermDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CourseTerm.objects.all()
    serializer_class = CourseTermSerializer
    permission_classes = permission_classes = [IsItManager, IsDeputyEducational]
    pagination_class = CustomPageNumberPagination

def get_current_term():
    today = timezone.now().date()
    try:
        # Finding a term where the current date falls between the start and end dates
        current_term = Term.objects.get(start_classes__lte=today, end_classes__gte=today)
        return current_term
    except Term.DoesNotExist:
        return None


class AvailableCoursesList(ListAPIView):
    serializer_class = CourseTermSerializer
    permission_classes = [IsAuthenticated, IsStudent]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        student_id = self.kwargs['pk']
        if student_id == 'me':
            student_id = self.request.user.pk
        student = Student.objects.get(pk=student_id)

        current_term = get_current_term()

        course_ids_for_term = CourseTerm.objects.filter(term=current_term).values_list('course', flat=True)

        return Course.objects.filter(id__in=course_ids_for_term).exclude(id__in=student.passed_courses.all()).exclude(
            id__in=student.current_courses.all())


class PassedCoursesReport(APIView):
    permission_classes = [IsAuthenticated, OR(IsAdminOrEducationalDeputyOrAdvisor, IsStudent)]

    def get(self, request, pk):
        try:
            student = Student.objects.get(pk=pk)
            passed_courses = student.passed_courses.all()
            serializer = CourseSerializer(passed_courses, many=True)
            return Response(serializer.data)
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CurrentCoursesList(APIView):
    permission_classes = [IsAuthenticated, OR(IsAdminOrEducationalDeputyOrAdvisor, IsStudent)]

    def get(self, request, pk):
        try:
            student = Student.objects.get(pk=pk)
            current_courses = student.current_courses.all()
            serializer = CourseSerializer(current_courses, many=True)
            return Response(serializer.data)
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RemainingYearsOfStudy(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def get(self, request, pk=None):
        if pk == 'me':
            pk = request.user.pk

        student = Student.objects.get(pk=pk)
        current_year = datetime.now().year
        remaining_years = 4 - (current_year - student.entry_year)
        return Response({'remaining_years': remaining_years})
