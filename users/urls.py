from django.urls import path
from .views import LoginApiView, LogoutApiView, ChangePasswordRequestApiView, ChangePasswordActionApiView

urlpatterns = [
    path('login/', LoginApiView.as_view(), name="login"),
    path('logout/', LogoutApiView.as_view(), name="logout"),
    path('change-password-request/', ChangePasswordRequestApiView.as_view(), name="change-password-request"),
    path('change-password-action/', ChangePasswordActionApiView.as_view(), name="change-password-action")
]