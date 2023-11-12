from django.urls import path
from . import views

app_name = 'student_requests'

urlpatterns = [
    path('subjects/', views.CourseListCreate.as_view(), name="course-list-create"),
    path('subjects/<int:pk>/', views.CourseRetrieveUpdateDelete.as_view(), name="course-get-update-delete"),
    path('student/<int:pk>/class-schedule/', views.ClassSchedulesView.as_view(), name="professor-class-schedule"),
    path('student/me/class-schedule/', views.ClassSchedulesView.as_view(), name="student-class-schedule"),
    path('student/<int:pk>/exam-schedule/', views.ExamSchedulesView.as_view(), name="professor-exam-schedule"),
    path('student/me/exam-schedule/', views.ExamSchedulesView.as_view(), name="student-exam-schedule"),
    # Assistant Remove Term
    path('assistant/remove-term/', views.AssistantRemoveTermList.as_view(), name='remove-term-list'),
    path('assistant/<int:term_id>/remove-term/<int:student_id>/', views.AssistantRemoveTermStudentDetail.as_view(), name='remove-term-detail'),
]