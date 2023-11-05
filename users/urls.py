from django.urls import path
from .views import StudentViewset
from . import views
app_name = 'users'

urlpatterns = [
    # Create - List - Retrieve - Update - Delete (Student) BY ITManager
    path('admin/students/', StudentViewset.as_view({'get':'list', 'post': 'create'}), name='student-list'),
    path('admin/students/<int:pk>/', StudentViewset.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update'}), name='student-detail'),
    # Educational Deputy can access students list and a student data details
    path('educational-deputy/student/', views.EducationalDeputyStudentsList.as_view(), name='educational-Deputy-students-list'),
    path('educational-deputy/student/<int:pk>/', views.EducationalDeputyStudentDetail.as_view(), name='educational-Deputy-student-detail'),
    # Educational Deputy can access to Professors list and a Professor data details
    path('educational-deputy/professors/', views.EducationalDeputyProfessorsList.as_view(), name='educational-Deputy-professors-list'),
    path('educational-deputy/professors/<int:pk>/', views.EducationalDeputyProfessorDetail.as_view(), name='educational-Deputy-professor-detail'),
] 
