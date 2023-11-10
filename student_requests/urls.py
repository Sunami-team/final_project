from django.urls import path
from .views import CourseListCreate, CourseRetrieveUpdateDelete, ClassSchedulesList

urlpattern = [
    path('subjects/', CourseListCreate.as_view(), name="course-list-create"),
    path('subjects/<int:pk>/', CourseRetrieveUpdateDelete.as_view(), name="course-get-update-delete"),
    path('student/<slug:student_id>/', ClassSchedulesList.as_view(), name="class-schedule-get"),
]