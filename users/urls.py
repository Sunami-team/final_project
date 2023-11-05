from django.urls import path

from users.views import FacultiesInformation, FacultiesListCreate

urlpatterns = [
    path('faculties/', FacultiesListCreate.as_view()),
    path('faculties/<pk>', FacultiesInformation.as_view()),
]
