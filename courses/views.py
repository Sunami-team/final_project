from rest_framework import viewsets
from rest_framework.generics import RetrieveAPIView
from .models import Term
from .serializers import TermSerializer
from rest_framework import generics
from .serializers import CourseSelectionSerializer
from django.db.models import Sum
from django.utils import timezone
from .models import Term, StudentCourse, CourseTerm
from .serializers import CourseSelectionSerializer, TermSerializer, StudentCourseSerializer, CourseTermSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, generics
import pandas as pd
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from users.permissions import IsProfessor
from rest_framework.viewsets import ModelViewSet
from users.permissions import IsItManager, IsDeputyEducational
from .permissions import IsItManager
from django.utils.translation import gettext as _
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from users.pagination import CustomPageNumberPagination
from datetime import datetime


class TermDetailAPIView(generics.RetrieveAPIView):
    queryset = Term.objects.all()
    serializer_class = TermSerializer


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


