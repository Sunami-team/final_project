from django.urls import path
from . import views

urlpatterns = [
    path('professor/<int:pk>/coures/<int:c_pk>/scores/', views.PostScoresApiView.as_view(), name="post-scores"),
    path('v1/term/<int:pk>/', views.TermViewSet.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update'}), name='term-detail'),
    path('courses/<int:term_id>/term/', views.CourseTermList.as_view(), name="course_term"),
    path('courses/<int:pk>/', views.CourseTermDetail.as_view(), name="course_term_detail"),  
]
