from django.urls import path
from . import views

urlpatterns = [
    path('professor/<int:pk>/coures/<int:c_pk>/scores/', views.PostScoresApiView.as_view(), name="post-scores"),
    path('v1/term/<int:pk>/', views.TermViewSet.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update'}), name='term-detail'),
]
