from django.db.models import Sum
from django.utils import timezone
from .models import Term, StudentCourse, CourseTerm
from .serializers import CourseSelectionSerializer, TermSerializer, StudentCourseSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, generics
import pandas as pd
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from users.permissions import IsProfessor
from rest_framework.viewsets import ModelViewSet
from .permissions import IsItManager
from django.utils.translation import gettext as _

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
            return Response({_('error'): 'زمان انتخاب واحد به پایان رسیده است.'}, status=status.HTTP_400_BAD_REQUEST)

        # بررسی تعداد واحدهای حداکثر و حداقل
        min_credit_units = 12  # حداقل تعداد واحدهای مجاز
        max_credit_units = 20  # حداکثر تعداد واحدهای مجاز
        selected_units = request.data.get('units', 0)
        if not (min_credit_units <= selected_units <= max_credit_units):
            return Response({_('error'): 'تعداد واحدهای انتخاب شده نامعتبر است.'}, status=status.HTTP_400_BAD_REQUEST)

        # بررسی شرایط پیش‌نیازی
        prerequisites = request.data.get('prerequisites', [])
        for prerequisite_id in prerequisites:
            if not student.passed_courses.filter(id=prerequisite_id).exists():
                return Response({_('error'): 'شما شرایط پیش‌نیاز را برآورده نکرده‌اید.'},
                                status=status.HTTP_400_BAD_REQUEST)

        # بررسی وضعیت دروس
        ongoing_courses = student.current_courses.filter(term=term)
        if len(ongoing_courses) > 0:
            return Response({_('error'): 'شما قبلاً دروسی را در این ترم انتخاب کرده‌اید.'},
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
                return Response({_('error'): 'تعداد واحدهای انتخاب شده بیشتر از حداکثر مجاز است.'},
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
        return Response({_('message'): 'دانشجو هنوز فرم انتخاب واحد ایجاد نکرده است.'}, status=status.HTTP_404_NOT_FOUND)


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
            return Response({_("error"): _("No file provided")}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Read the Excel file into a DataFrame
            df = pd.read_excel(file)

            # Get the course term using the provided professor and course IDs
            course_term = CourseTerm.objects.get(professor=pk, course=c_pk)

            # Loop through the rows in the DataFrame and update the grades
            for index, row in df.iterrows():
                student_name = row['student']
                grade = row['grade']

                # Assuming you have a proper way to match students by name
                student = StudentCourse.objects.get(student__full_name=student_name, course_term=course_term)

                # Update the grade for the student
                student.grade = grade
                student.save()

            return Response({_("message"): _("Grades updated successfully")}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({_("error"): str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TermViewSet(ModelViewSet):
    serializer_class = TermSerializer
    queryset = Term.objects.all().prefetch_related(
        'termstudentprofessor_set__students', 'termstudentprofessor_set__professors')
    permission_classes = [IsItManager]


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
            return Response({_('error'): 'زمان انتخاب واحد به پایان رسیده است.'}, status=status.HTTP_400_BAD_REQUEST)

        # بررسی تعداد واحدهای حداکثر و حداقل
        min_credit_units = 12  # حداقل تعداد واحدهای مجاز
        max_credit_units = 20  # حداکثر تعداد واحدهای مجاز
        selected_units = request.data.get('units', 0)
        if not (min_credit_units <= selected_units <= max_credit_units):
            return Response({_('error'): 'تعداد واحدهای انتخاب شده نامعتبر است.'}, status=status.HTTP_400_BAD_REQUEST)

        # بررسی شرایط پیش‌نیازی
        prerequisites = request.data.get('prerequisites', [])
        for prerequisite_id in prerequisites:
            if not student.passed_courses.filter(id=prerequisite_id).exists():
                return Response({_('error'): 'شما شرایط پیش‌نیاز را برآورده نکرده‌اید.'},
                                status=status.HTTP_400_BAD_REQUEST)

        # بررسی وضعیت دروس
        ongoing_courses = student.current_courses.filter(term=term)
        if len(ongoing_courses) > 0:
            return Response({_('error'): 'شما قبلاً دروسی را در این ترم انتخاب کرده‌اید.'},
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
                return Response({_('error'): 'تعداد واحدهای انتخاب شده بیشتر از حداکثر مجاز است.'},
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
        return Response({_('message'): 'دانشجو هنوز فرم انتخاب واحد ایجاد نکرده است.'}, status=status.HTTP_404_NOT_FOUND)


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
            return Response({_("error"): _("No file provided")}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Read the Excel file into a DataFrame
            df = pd.read_excel(file)

            # Get the course term using the provided professor and course IDs
            course_term = CourseTerm.objects.get(professor=pk, course=c_pk)

            # Loop through the rows in the DataFrame and update the grades
            for index, row in df.iterrows():
                student_name = row['student']
                grade = row['grade']

                # Assuming you have a proper way to match students by name
                student = StudentCourse.objects.get(student__full_name=student_name, course_term=course_term)

                # Update the grade for the student
                student.grade = grade
                student.save()

            return Response({_("message"): _("Grades updated successfully")}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({_("error"): str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)