from django.urls import path
from . import views

# from .models import EmergencyDropRequestView, EmergencyDropRequestListView, EmergencyDropRequestDetailView, EmergencyDropRequestApprovalView

app_name = "student_requests"

urlpatterns = [

    path('student/me/class-schedule/', views.ClassScheduleViewSet.as_view({'get':'list'}), name="class-schedule"),
    path('student/me/exam-schedule/', views.ExamScheduleViewSet.as_view({'get':'list'}), name="exam-schedule"),

    # Assistant Remove Term
    path(
        "assistant/remove-term/",
        views.AssistantRemoveTermList.as_view(),
        name="remove-term-list",
    ),
    path(
        "assistant/<int:term_id>/remove-term/<int:student_id>/",
        views.AssistantRemoveTermStudentDetail.as_view(),
        name="remove-term-detail",
    ),
    # emergency drop request
    path(
        "student/<int:pk>/courses/<int:c_pk>/emergency-remove/",
        views.EmergencyDropRequestView.as_view(),
        name="emergency-remove_",
    ),
    path(
        "assistant/<str:pk>/emergency-remove/",
        views.EmergencyDropRequestListView.as_view(),
        name="emergency-request-list",
    ),
    path(
        "assistant/<str:pk>/emergency-remove/<int:s_pk>/",
        views.EmergencyDropRequestDetailView.as_view(),
        name="emergency-request-detail",
    ),
    path(
        "assistant/<str:pk>/emergency-remove/<int:s_pk>/approve-reject",
        views.EmergencyDropRequestApprovalView.as_view(),
        name="emergency-request-approve-reject",
    ),
    # Assistant approve Grade Reconsideration
    path(
        "assistant/<int:professor_id>/courses/<int:course_id>/prof-approved/",
        views.AssistantGradeReconsiderationRequestList.as_view(),
        name="assistant-change-grade-list",
    ),
    path(
        "assistant/<int:professor_id>/courses/<int:course_id>/prof-approved/<int:student_id>/",
        views.AssistantGradeReconsiderationRequestStudentDetail.as_view(),
        name="assistant-change-grade-list-student-detail",
    ),
    # Courses Correction Student Request
    path(
        "student/<int:pk>/course-substitution/create/",
        views.CreateCorrectionRequestByStudent.as_view(),
        name="correction-request",
    ),
    path(
        "student/<int:pk>/course-substitution/",
        views.DetailCorrectionRequestByStudent.as_view(),
        name="see-correction-request",
    ),
    path(
        "student/<int:pk>/course-substitution/<int:term_id>/check/",
        views.CorrectionShowErrors.as_view(),
        name="correction-errors-list",
    ),
    path(
        "student/<int:pk>/course-substitution/submit/",
        views.CorrectionSubmit.as_view(),
        name="correction-student-submit",
    ),
    path(
        "student/<int:pk>/course-substitution/send-form/<int:term_id>/",
        views.CorrectionSendForm.as_view(),
        name="correction-send-form",
    ),
    # Military Service Student Request
    path(
        "student/<int:student_id>/studying-evidence/",
        views.MilitaryServiceRequestViewSet.as_view(
            {"post": "create", "get": "retrieve", "delete": "destroy", "put": "update"}
        ),
    ),
    # professor approve Grade Reconsideration
    path(
        "professor/<int:professor_id>/courses/<int:course_id>/appeal-requests/",
        views.GradeReconsiderationRequestViewSet.as_view({"get": "list"}),
        name="grade-reconsideration-list",
    ),
    path(
        "professor/<int:professor_id>/courses/<int:course_id>/appeal-requests/<int:student_id>/",
        views.GradeReconsiderationRequestViewSet.as_view(
            {"get": "retrieve", "post": "create"}
        ),
        name="grade-reconsideration-detail",
    ),
    path(
        "professor/<int:professor_id>/courses/<int:course_id>/approve/",
        views.GradeReconsiderationRequestViewSet.as_view({"post": "create"}),
        name="grade-approval",
    ),
    path(
        "student/<int:student_id>/courses/<int:course_id>/appeal-request/",
        views.GradeReconsiderationRequestView.as_view(),
        name="student-reconsideration",
    ),
    path(
        'assistant/<str:pk_or_me>/studying-evidence/',
        views.StudentRequestList.as_view(),
        name="military-service-request-list"
    ),
    path(
        'assistant/<str:pk_or_me>/studying-evidence/<int:s_pk>/',
        views.StudentRequestDetail.as_view(),
        name="military-service-request-detail"
    ),
    path(
        'assistant/<int:d_pk>/studying-evidence-update/<int:pk>/',
        views.MilitaryServiceRequestApproval.as_view(),
        name="military-service-request-approval"
    ),
    path('assistant/<str:pk_or_me>/studying-evidence/', views.StudentRequestList.as_view()),
    path('assistant/<str:pk_or_me>/studying-evidence/<int:s_pk>/', views.StudentRequestDetail.as_view()),
    path('professor/<int:professor_id>/students-selection-forms/', views.StudentSelectionForm.as_view()),
    path('professor/<int:professor_id>/students-selection-forms/<int:student_id>/term/<int:term_id>', views.StudentSelectionFormDetailAndApproveRejection.as_view()),
    
    path('professor/<int:pk>/course-correction-requests/',
         views.CourseCorrectionRequestView.as_view({'get': 'list'}), name='course-correction-requests'),
    path('professor/<int:pk>/students-substitution-forms/<int:s_pk>/',
         views.CourseCorrectionRequestView.as_view({'get': 'retrieve'}), name='correction-detail'),
]
