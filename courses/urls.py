from django.url import path
from . import views

urlpatterns = [
    ('professor/<int:pk>/coures/<int:c_pk>/scores/', views.PostScoresApiView.as_view(), name="post-scores"),
]
