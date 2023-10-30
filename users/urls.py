from django.urls import path
from .views import StudentViewset
from . import views
app_name = 'users'

urlpatterns = [
    # Create - List - Retrieve - Update - Delete (Student) BY ITManager
    path('admin/students/', StudentViewset.as_view({'get':'list', 'post': 'create'}), name='student-list'),
    path('admin/students/<int:pk>/', StudentViewset.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update'}), name='student-detail'),
    path('admin/professors/', views.ProfessorListView.as_view(), name='list_professors_v1'),
    path('admin/professors/create/', views.ProfessorCreateView.as_view(), name='create_professor_v1'),
    path('admin/professors/<int:pk>/', views.ProfessorRetrieveView.as_view(), name='professor_retrieve_v1'),
    path('admin/professors/<int:pk>/update/', views.ProfessorUpdateView.as_view(), name='professor_update_v1'),
    path('admin/professors/<int:pk>/delete/', views.ProfessorDeleteView.as_view(), name='professor_delete_v1'),
] 
