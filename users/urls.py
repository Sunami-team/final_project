from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    # Auth
    path("register/", views.RegistrationApiView.as_view(), name="register"),
    path("login/", views.LoginApiView.as_view(), name="login"),
    path("logout/", views.LogoutApiView.as_view(), name="logout"),
    path(
        "change-password-request/",
        views.ChangePasswordRequestApiView.as_view(),
        name="change-password-request",
    ),
    path(
        "change-password-action/",
        views.ChangePasswordActionApiView.as_view(),
        name="change-password-action",
    ),
    # Create - List - Retrieve - Update - Delete (Student) BY ITManager
    path(
        "admin/students/",
        views.StudentViewset.as_view({"get": "list", "post": "create"}),
        name="student-list",
    ),
    path(
        "admin/students/<int:pk>/",
        views.StudentViewset.as_view(
            {"get": "retrieve", "delete": "destroy", "put": "update"}
        ),
        name="student-detail",
    ),
    path("register/", views.RegistrationApiView.as_view(), name="register"),
    path("login/", views.LoginApiView.as_view(), name="login"),
    path("logout/", views.LogoutApiView.as_view(), name="logout"),
    path(
        "change-password-request/",
        views.ChangePasswordRequestApiView.as_view(),
        name="change-password-request",
    ),
    path(
        "change-password-action/",
        views.ChangePasswordActionApiView.as_view(),
        name="change-password-action",
    ),
    # Create - List - Retrieve - Update - Delete (Student) BY ITManager
    path(
        "admin/students/",
        views.StudentViewset.as_view({"get": "list", "post": "create"}),
        name="student-list",
    ),
    path(
        "admin/students/<int:pk>/",
        views.StudentViewset.as_view(
            {"get": "retrieve", "delete": "destroy", "put": "update"}
        ),
        name="student-detail",
    ),
    path(
        "admin/professors/",
        views.ProfessorListView.as_view(),
        name="list_professors_v1",
    ),
    path(
        "admin/professors/create/",
        views.ProfessorCreateView.as_view(),
        name="create_professor_v1",
    ),
    path(
        "admin/professors/<int:pk>/",
        views.ProfessorRetrieveView.as_view(),
        name="professor_retrieve_v1",
    ),
    path(
        "admin/professors/<int:pk>/update/",
        views.ProfessorUpdateView.as_view(),
        name="professor_update_v1",
    ),
    path(
        "admin/professors/<int:pk>/delete/",
        views.ProfessorDeleteView.as_view(),
        name="professor_delete_v1",
    ),
    path("faculties/", views.FacultiesListCreate.as_view()),
    path("faculties/<pk>", views.FacultiesInformation.as_view()),
    # Educational Deputy can access students list and a student data details
    path(
        "educational-deputy/student/",
        views.EducationalDeputyStudentsList.as_view(),
        name="educational-Deputy-students-list",
    ),
    path(
        "educational-deputy/student/<int:pk>/",
        views.EducationalDeputyStudentDetail.as_view(),
        name="educational-Deputy-student-detail",
    ),
    # Educational Deputy can access to Professors list and a Professor data details
    path(
        "educational-deputy/professors/",
        views.EducationalDeputyProfessorsList.as_view(),
        name="educational-Deputy-professors-list",
    ),
    path(
        "educational-deputy/professors/<int:pk>/",
        views.EducationalDeputyProfessorDetail.as_view(),
        name="educational-Deputy-professor-detail",
    ),
    # Update student and professor info
    path(
        "students/<int:pk>",
        views.StudentInfoViewSet.as_view({"get": "retrieve", "put": "update"}),
        name="student-detail",
    ),
    path(
        "professors/<int:pk>",
        views.ProfessorInfoViewSet.as_view({"get": "retrieve", "put": "update"}),
        name="professor-detail",
    ),
    
    # Create - List - Retrieve - Update - Delete (Term) BY ITManager
    path('admin/term/', views.TermViewSet.as_view({'get': 'list', 'post': 'create'}), name='term-list'), 
    path('admin/term/<int:pk>/', views.TermViewSet.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update'}), name='term-detail'),
]

