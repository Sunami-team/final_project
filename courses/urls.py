from django.urls import path
from . import views
from .views import AvailableCoursesList, CurrentCoursesList, RemainingYearsOfStudy, PassedCoursesReport

urlpatterns = [
    path("subjects/", views.CourseListCreate.as_view(), name="course-list-create"),
    path(
        "subjects/<int:pk>/",
        views.CourseRetrieveUpdateDelete.as_view(),
        name="course-get-update-delete",
    ),
    path(
        "professor/<int:pk>/coures/<int:c_pk>/scores/",
        views.PostScoresApiView.as_view(),
        name="post-scores",
    ),
    path(
        "v1/term/<int:pk>/",
        views.TermViewSet.as_view(
            {"get": "retrieve", "delete": "destroy", "put": "update"}
        ),
        name="term-detail",
    ),
    path('courses/<int:term_id>/term/', views.CourseTermList.as_view(), name="course_term"),
    path('courses/<int:pk>/', views.CourseTermDetail.as_view(), name="course_term_detail"),
    path('student/<str:pk>/my-course/', AvailableCoursesList.as_view(), name='available-courses'),
    path('student/<str:pk>/pass-courses-report/', PassedCoursesReport.as_view(), name='passed-courses-report'),
    path('student/<str:pk>/term-courses/', CurrentCoursesList.as_view(), name='current-courses'),
    path('student/<str:pk>/remaining-terms/', RemainingYearsOfStudy.as_view(), name='remaining-years-of-study'),

]
