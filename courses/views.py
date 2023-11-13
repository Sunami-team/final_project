from django.db.models import Sum
from django.utils import timezone
from .models import Term, StudentCourse, CourseTerm
from .serializers import CourseSelectionSerializer, TermSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Course, Term, StudentCourse, StudyField

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

class CourseSubstitutionCheck(APIView):
    def post(self, request, pk):
        try:
            selected_course_id = request.data.get('selected_course')
            term_id = request.data.get('term')
            student_id = request.data.get('student')

            # شرط: درس ͖یشنیاز حتما باید در وضعیت قبول باشد.
            prerequisite_course_id = request.data.get('prerequisite')
            if prerequisite_course_id:
                prerequisite_course = Course.objects.get(pk=prerequisite_course_id)
                if prerequisite_course.status != 'Accepted':
                    raise Exception("Prerequisite course must be in 'Accepted' status.")

            # شرط: درس تکراری یا پاس شده نمیتوان برداشت.
            selected_course = Course.objects.get(pk=selected_course_id)
            student_courses = StudentCourse.objects.filter(student_id=student_id, term_id=term_id)
            for course in student_courses:
                if course.course_term.course_id == selected_course_id and course.course_status in ['pass', 'failed']:
                    raise Exception("Cannot take a course that is passed or failed.")

            # شرط: درس تکمیل را نمیتوان اخذ کرد.
            if selected_course.status == 'Completed':
                raise Exception("Cannot take a completed course.")

            # شرط: درس همنیاز را نمیتوان زودتر از درسی که همنیاز آن شده حذف کرد.
            if selected_course.prerequisites.filter(course_id=prerequisite_course_id).exists():
                raise Exception("Cannot remove a prerequisite course before completing its prerequisite.")

            # شرط: تداخل زمانی در امتحان و کلاس نباید وجود داشته باشد.
            # اینجا فرض می‌شود که اطلاعات زمان کلاسها و امتحانات در دیتابیس ذخیره شده است.
            term = Term.objects.get(pk=term_id)
            conflicting_courses = CourseTerm.objects.filter(term=term, class_day=request.data['class_day'],
                                                            class_time=request.data['class_time'])
            if conflicting_courses.exists():
                raise Exception("Class time conflict with another course.")

            # شرط: دانشجو تنها میتواند ۶ واحد حذف و ۶ واحد اضافه کند و حداکثر دو درس را میتواند حذف و دو درس را اضافه کند.
            units_to_add = request.data.get('units_to_add', 0)
            units_to_remove = request.data.get('units_to_remove', 0)
            courses_to_add = request.data.get('courses_to_add', 0)
            courses_to_remove = request.data.get('courses_to_remove', 0)

            if units_to_add > 6 or units_to_remove > 6:
                raise Exception("Cannot add or remove more than 6 units.")

            if courses_to_add > 2 or courses_to_remove > 2:
                raise Exception("Cannot add or remove more than 2 courses.")

            # شرط: تنها دروس مرتبط به رشته را میتوان برداشت.
            study_field = StudyField.objects.get(pk=request.data.get('study_field'))
            if not selected_course.related_to_major(study_field):
                raise Exception("Can only take courses related to the major.")

            # هر خطای منطقی میباید یادهسازی شود.

            return Response({"message": "Changes checked successfully"}, status=status.HTTP_200_OK)

        except Course.DoesNotExist:
            return Response({"error": "Invalid course ID"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
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
