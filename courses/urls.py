from django.urls import path
from . import views

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
    # path('courses/<int:pk>/', views.CourseTermDetail.as_view(), name="course_term_detail"), #TODO: Amin Hosseini
]
