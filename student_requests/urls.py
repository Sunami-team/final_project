from django.urls import path
from . import views

app_name = 'student_requests'

urlpatterns = [
    path('student/<int:pk>/course-substitution/create/', views.CreateCorrectionRequestByStudent.as_view(), name='correction-request'),
    path('student/<int:pk>/course-substitution/', views.DetailCorrectionRequestByStudent.as_view(), name='see-correction-request'),
    path('student/<int:pk>/course-substitution/check/', views.CorrectionShowErrors.as_view(), name='correction-errors-list'),
    # Assistant Remove Term
    path('assistant/remove-term/', views.AssistantRemoveTermList.as_view(), name='remove-term-list'),
    path('assistant/remove-term/<int:pk>/', views.AssistantRemoveTermStudentDetail.as_view(), name='remove-term-detail'),
]
