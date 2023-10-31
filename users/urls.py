from django.urls import path
from .views import LoginApiView, LogoutApiView, ChangePasswordRequestApiView, ChangePasswordActionApiView, StudentViewset

app_name = 'users'
<<<<<<< HEAD
urlpatterns = [
    path('login/', LoginApiView.as_view(), name="login"),
    path('logout/', LogoutApiView.as_view(), name="logout"),
    path('change-password-request/', ChangePasswordRequestApiView.as_view(), name="change-password-request"),
    path('change-password-action/', ChangePasswordActionApiView.as_view(), name="change-password-action")
    # Create - List - Retrieve - Update - Delete (Student) BY ITManager
    path('admin/students/', StudentViewset.as_view({'get':'list', 'post': 'create'}), name='student-list'),
    path('admin/students/<int:pk>/', StudentViewset.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update'}), name='student-detail'),
]
