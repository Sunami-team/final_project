from django.urls import path
from .views import StudentViewset

app_name = 'users'

urlpatterns = [
    # Create - List - Retrieve - Update - Delete (Student) BY ITManager
    path('v1/student/', StudentViewset.as_view({'get':'list', 'post': 'create'}), name='student-list'),
    path('v1/student/<int:pk>/', StudentViewset.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update'}), name='student-detail'),
] 
