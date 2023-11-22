from django.shortcuts import render
from users.permissions import (
    IsItManager,
    IsDeputyEducational,
    IsStudentOrDeputyEducational,
    IsProfessorOrDeputyEducational,
    IsStudent,
    IsProfessor,
)
from .serializers import *
from django.contrib.auth import authenticate, login, logout
from rest_framework import generics, status, viewsets
from .models import (
    User,
    ChangePasswordToken,
    Student,
    DeputyEducational,
    Professor,
    ITManager,
)
from courses.models import Faculty
from rest_framework import generics, status, viewsets
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
import random
from .pagination import CustomPageNumberPagination
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .tasks import send_email
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from django.utils.translation import gettext as _
from rest_framework.exceptions import NotFound
from rest_framework.viewsets import ModelViewSet
# I add this comment to commit and remove migration files


class AssistanList(generics.ListAPIView):
    """
    Assistant List API View
    """

    queryset = DeputyEducational.objects.all()
    serializer_class = AssistanSerializer


class AssistanDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Assistant Detail API View
    """

    queryset = DeputyEducational.objects.all()
    serializer_class = AssistanSerializer


class AssistanCreate(generics.CreateAPIView):
    """
    Assistant Create API View
    """

    queryset = DeputyEducational.objects.all()
    serializer_class = AssistanSerializer


class AssistanUpdate(generics.UpdateAPIView):
    """
    Assistant Update API View
    """

    queryset = DeputyEducational.objects.all()
    serializer_class = AssistanSerializer


class AssistanDelete(generics.DestroyAPIView):
    """
    Assistant Delete API View
    """

    queryset = DeputyEducational.objects.all()
    serializer_class = AssistanSerializer


class RegistrationApiView(generics.CreateAPIView):
    """
    This API is for user registration using CreateAPIView
    """

    serializer_class = RegistrationSerializer

    def perform_create(self, serializer):
        user_type = self.request.data.get("user_type")

        # Create user based on the selected type
        if user_type == "student":
            user = Student.objects.create_user(**serializer.validated_data)
        elif user_type == "professor":
            user = Professor.objects.create_user(**serializer.validated_data)
        elif user_type == "it_manager":
            user = ITManager.objects.create_user(**serializer.validated_data)
        elif user_type == "deputy_educational":
            user = DeputyEducational.objects.create_user(**serializer.validated_data)

        # You may want to handle any additional user-specific data here

        token, created = Token.objects.get_or_create(user=user)
        response_data = {"token": token.key, "user": user.username}
        return Response(response_data, status=status.HTTP_201_CREATED)


class LoginApiView(generics.GenericAPIView):
    """
    This API is for login using GenericAPIView
    """

    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        login(request, user)

        token, created = Token.objects.get_or_create(user=user)
        response_data = {"token": token.key, "user": user.username}
        return Response(response_data, status=status.HTTP_200_OK)


class LogoutApiView(generics.GenericAPIView):
    """
    This API is for logout using GenericAPIView
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        Token.objects.get(user=request.user).delete()
        return Response(
            {_("message"): _("You have been successfully logged out.")},
            status=status.HTTP_200_OK,
        )


class ChangePasswordRequestApiView(generics.GenericAPIView):
    """
    This API is for change password request using GenericAPIView
    """

    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        user = request.user
        user_email = user.email
        print(user_email)  # print out the recipient email
        token = random.randint(1000, 10000)
        ChangePasswordToken.objects.create(user=user, token=token)
        send_email.delay(user_email, token)  # shared task by celery
        return Response(
            {_("token"): token, _("detail"): _("Token generated successfully")},
            status=status.HTTP_200_OK,
        )


class ChangePasswordActionApiView(generics.UpdateAPIView):
    """
    This API is for change password action using GenericAPIView
    """

    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        user = self.request.user
        token = self.request.data["token"]
        return ChangePasswordToken.objects.get(user=user, token=token)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        new_password = request.data["new_password"]

        user = instance.user
        user.set_password(new_password)
        user.save()

        instance.delete()

        return Response(
            {_("detail"): _("Password changed successfully")}, status=status.HTTP_200_OK
        )


class StudentViewset(viewsets.ModelViewSet):
    """
    This viewset is for Create, List, Retrieve, Updtate, Delete  --> Student
    """

    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    permission_classes = [IsItManager]
    pagination_class = CustomPageNumberPagination

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = {
        "first_name": ["exact", "in"],
        "last_name": ["exact", "in"],
        "national_id": ["exact"],
        "college": ["exact"],
        "study_field": ["exact"],
        "entry_year": ["exact"],
        "military_status": ["exact"],
        "personal_number": ["exact"],
    }
    search_fields = ["first_name", "last_name"]
    ordering_fields = ["id", "last_name"]


class ProfessorListView(generics.ListAPIView):
    """
    Professor List API View
    """

    queryset = Professor.objects.all().order_by("id")
    serializer_class = ProfessorSerializer
    permission_classes = [IsItManager]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        # page_size = self.request.query_params.get('page_size', 10)

        first_name = self.request.query_params.get("first_name", None)
        last_name = self.request.query_params.get("last_name", None)
        professor_id = self.request.query_params.get("professor_id", None)
        national_id = self.request.query_params.get("national_id", None)
        faculty = self.request.query_params.get("faculty", None)
        study_field = self.request.query_params.get("study_field", None)
        rank = self.request.query_params.get("rank", None)

        if first_name:
            queryset = queryset.filter(user__first_name__icontains=first_name)
        if last_name:
            queryset = queryset.filter(user__last_name__icontains=last_name)
        if professor_id:
            queryset = queryset.filter(id=professor_id)
        if national_id:
            queryset = queryset.filter(user__national_id=national_id)
        if faculty:
            queryset = queryset.filter(faculty__name=faculty)
        if study_field:
            queryset = queryset.filter(study_field__name=study_field)
        if rank:
            queryset = queryset.filter(rank=rank)
        return queryset


class ProfessorCreateView(generics.CreateAPIView):
    """
    Professor Create API View
    """

    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    permission_classes = [IsItManager]


class ProfessorRetrieveView(generics.RetrieveAPIView):
    """
    Professor Retrieve API View
    """

    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    permission_classes = [IsItManager]


class ProfessorUpdateView(generics.UpdateAPIView):
    """
    Professor Update API View
    """

    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    permission_classes = [IsItManager]


class ProfessorDeleteView(generics.DestroyAPIView):
    """
    Professor Delete API View
    """

    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    permission_classes = [IsItManager]
    ordering_fields = ["id", "last_name"]


class FacultiesListCreate(generics.ListCreateAPIView):
    """
    Faculty Create and List API View
    """

    queryset = Faculty.objects.all()
    serializer_class = FacultiesListSerializer
    permission_class = [IsItManager]
    pagination_class = CustomPageNumberPagination


class FacultiesInformation(generics.RetrieveUpdateDestroyAPIView):
    """
    Faculty Retrieve API View
    """

    queryset = Faculty.objects.all()
    serializer_class = FacultiesListSerializer


# Show Students List , Access By Educational Deputy


class EducationalDeputyStudentsList(generics.ListAPIView):
    """
    Deputy Educational Access to students List
    """

    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    pagination_class = CustomPageNumberPagination
    permission_classes = [IsDeputyEducational]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = {
        "first_name": ["exact", "in"],
        "last_name": ["exact", "in"],
        "national_id": ["exact"],
        "college": ["exact"],
        "study_field": ["exact"],
        "entry_year": ["exact"],
        "military_status": ["exact"],
        "personal_number": ["exact"],
    }
    search_fields = ["first_name", "last_name"]
    ordering_fields = ["id", "last_name"]


class EducationalDeputyStudentDetail(generics.RetrieveAPIView):
    """
    Deputy Educational Access to a student Data Detail
    """

    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    permission_classes = [IsStudentOrDeputyEducational]


class EducationalDeputyProfessorsList(generics.ListAPIView):
    serializer_class = DeputyEducationalProfessorSerializer
    queryset = Professor.objects.all()
    pagination_class = CustomPageNumberPagination
    permission_classes = [IsDeputyEducational]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = [
        "first_name",
        "last_name",
        "personal_number",
        "national_id",
        "study_field",
        "expertise",
        "rank",
    ]
    search_fields = ["first_name", "last_name"]
    ordering_fields = ["id", "last_name"]


class EducationalDeputyProfessorDetail(generics.RetrieveAPIView):
    serializer_class = DeputyEducationalProfessorSerializer
    queryset = Professor.objects.all()
    permission_classes = [IsProfessorOrDeputyEducational]


class StudentInfoViewSet(viewsets.ModelViewSet):
    serializer_class = StudentInfoSerializer
    permission_classes = [IsAuthenticated, IsStudent]

    def get_queryset(self):
        user_id = self.kwargs.get("pk")

        if not user_id:
            raise NotFound(_("Student ID not provided"))

        try:
            student = Student.objects.get(id=user_id)
        except Student.DoesNotExist:
            raise NotFound("Student not found")

        return Student.objects.filter(id=student.id)


class ProfessorInfoViewSet(viewsets.ModelViewSet):
    serializer_class = ProfessorInfoSerializer
    permission_classes = [IsAuthenticated, IsProfessor]

    def get_queryset(self):
        user_id = self.kwargs.get("pk")

        if not user_id:
            raise NotFound(_("Professor ID not provided"))

        try:
            professor = Professor.objects.get(id=user_id)
        except Professor.DoesNotExist:
            raise NotFound(ـ("Professor not found"))

        return Professor.objects.filter(id=professor.id)

      
class TermViewSet(ModelViewSet):
    serializer_class = TermSerializer
    queryset = Term.objects.all().prefetch_related('termstudentprofessor_set__students', 'termstudentprofessor_set__professors')
    permission_classes = [IsItManager]
