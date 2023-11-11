from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('register/', views.RegistrationApiView.as_view(), name="register"),
    path('login/', views.LoginApiView.as_view(), name="login"),
    path('logout/', views.LogoutApiView.as_view(), name="logout"),
    path('change-password-request/', views.ChangePasswordRequestApiView.as_view(), name="change-password-request"),
    path('change-password-action/', views.ChangePasswordActionApiView.as_view(), name="change-password-action"),
    # Create - List - Retrieve - Update - Delete (Student) BY ITManager
    path('admin/students/', views.StudentViewset.as_view({'get':'list', 'post': 'create'}), name='student-list'),
    path('admin/students/<int:pk>/', views.StudentViewset.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update'}), name='student-detail'),
    path('register/', views.RegistrationApiView.as_view(), name="register"),
    path('login/', views.LoginApiView.as_view(), name="login"),
    path('logout/', views.LogoutApiView.as_view(), name="logout"),
    path('change-password-request/', views.ChangePasswordRequestApiView.as_view(), name="change-password-request"),
    path('change-password-action/', views.ChangePasswordActionApiView.as_view(), name="change-password-action"),
    # Create - List - Retrieve - Update - Delete (Student) BY ITManager
    path('admin/students/', views.StudentViewset.as_view({'get':'list', 'post': 'create'}), name='student-list'),
    path('admin/students/<int:pk>/', views.StudentViewset.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update'}), name='student-detail'),
    path('admin/professors/', views.ProfessorListView.as_view(), name='list_professors_v1'),
    path('admin/professors/create/', views.ProfessorCreateView.as_view(), name='create_professor_v1'),
    path('admin/professors/<int:pk>/', views.ProfessorRetrieveView.as_view(), name='professor_retrieve_v1'),
    path('admin/professors/<int:pk>/update/', views.ProfessorUpdateView.as_view(), name='professor_update_v1'),
    path('admin/professors/<int:pk>/delete/', views.ProfessorDeleteView.as_view(), name='professor_delete_v1'),
    path('faculties/', views.FacultiesListCreate.as_view()),
    path('faculties/<pk>', views.FacultiesInformation.as_view()),
]
