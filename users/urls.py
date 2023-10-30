from django.urls import path
from .views import StudentViewset

app_name = 'users'

urlpatterns = [
    # Create - List - Retrieve - Update - Delete (Student) BY ITManager
    path('admin/students/', StudentViewset.as_view({'get':'list', 'post': 'create'}), name='student-list'),
    path('admin/students/<int:pk>/', StudentViewset.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update'}), name='student-detail'),
] 
