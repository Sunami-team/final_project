from django.test import TestCase
from rest_framework.test import APIClient
from users.models import User, DeputyEducational, Student, Professor
from courses.models import Faculty, StudyField, Term
from student_requests.models import TermDropRequest, GradeReconsiderationRequest
from courses.models import Course, CourseTerm, Faculty
from django.urls import reverse
from rest_framework import status

class CourseListCreateTest(TestCase):
    def setUp(self):
        self.it_manager = User.objects.create_user(
            username="it_manager",
            password="test123",
            email="123@yahoo.com",
            user_type="it_manager",
        )
        self.deputy_educational = User.objects.create_user(
            username="deputy_edu",
            password="test456",
            email="321@yahoo.com",
            user_type="deputy_educational",
        )
        self.college = Faculty.objects.create(name="fake_college")
        self.object = Course.objects.create(
            college=self.college, name="new_course", course_unit="3", course_type="O"
        )  # Create your test object

    def test_it_manager_access(self):
        self.client.force_login(self.it_manager)
        url = reverse("course-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_deputy_educational_access(self):
        self.client.force_login(self.deputy_educational)
        url = reverse("course-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
