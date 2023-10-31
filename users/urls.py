from django.urls import path
<<<<<<< HEAD
from .views import LoginApiView, LogoutApiView, ChangePasswordRequestApiView, ChangePasswordActionApiView

urlpatterns = [
    path('login/', LoginApiView.as_view(), name="login"),
    path('logout/', LogoutApiView.as_view(), name="logout"),
    path('change-password-request/', ChangePasswordRequestApiView.as_view(), name="change-password-request"),
    path('change-password-action/', ChangePasswordActionApiView.as_view(), name="change-password-action")
]
=======
from .views import StudentViewset

app_name = 'users'

urlpatterns = [
    # Create - List - Retrieve - Update - Delete (Student) BY ITManager
    path('admin/students/', StudentViewset.as_view({'get':'list', 'post': 'create'}), name='student-list'),
    path('admin/students/<int:pk>/', StudentViewset.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update'}), name='student-detail'),
] 
>>>>>>> b541cb0eb1ab4b6c4bd351bdc3cfaa5dfa7d43d3
