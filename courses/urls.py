from django.urls import path
from . import views

urlpatterns = [
    path('professor/<int:pk>/coures/<int:c_pk>/scores/', views.PostScoresApiView.as_view(), name="post-scores"),
]
