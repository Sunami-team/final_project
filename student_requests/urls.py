from django.urls import path
from . import views
from .models import EmergencyDropRequestView, EmergencyDropRequestListView, EmergencyDropRequestDetailView, \
    EmergencyDropRequestApprovalView

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
    # emergency drop request
    path('student/<int:pk>/courses/<int:c_pk>/emergency-remove/', EmergencyDropRequestView.as_view(), name='emergency-remove_'),
    path('assistant/<str:pk>/emergency-remove/', EmergencyDropRequestListView.as_view(), name='emergency-request-list'),
    path('assistant/<str:pk>/emergency-remove/<int:s_pk>/', EmergencyDropRequestDetailView.as_view(), name='emergency-request-detail'),
    path('assistant/<str:pk>/emergency-remove/<int:s_pk>/approve-reject', EmergencyDropRequestApprovalView.as_view(), name='emergency-request-approve-reject'),
    # Assistant approve Grade Reconsideration
    path('assistant/<int:professor_id>/courses/<int:course_id>/prof-approved/', views.AssistantGradeReconsiderationRequestList.as_view(), name='assistant-change-grade-list'),
    path('assistant/<int:professor_id>/courses/<int:course_id>/prof-approved/<int:student_id>/', views.AssistantGradeReconsiderationRequestStudentDetail.as_view(), name='assistant-change-grade-list-student-detail'),
    # Courses Correction Student Request
    path('student/<int:pk>/course-substitution/create/', views.CreateCorrectionRequestByStudent.as_view(), name='correction-request'),
    path('student/<int:pk>/course-substitution/', views.DetailCorrectionRequestByStudent.as_view(), name='see-correction-request'),
    path('student/<int:pk>/course-substitution/<int:term_id>/check/', views.CorrectionShowErrors.as_view(), name='correction-errors-list'),
    path('student/<int:pk>/course-substitution/submit/', views.CorrectionSubmit.as_view(), name='correction-student-submit'),
    path('student/<int:pk>/course-substitution/send-form/<int:term_id>/', views.CorrectionSendForm.as_view(), name='correction-send-form'),
]