from django.test import TestCase
from django.urls import reverse
from users.models import ITManager, User, Student, DeputyEducational, Professor
from rest_framework.test import APIClient
from courses.models import Faculty, StudyField
from datetime import datetime


class TestAdminStudentApi(TestCase):
    """This is test class is for Create, List, Retieve, Update, Delete a student By ITManager"""

    def setUp(self):
        self.client = APIClient()
        self.it_manager = ITManager.objects.create(
            username="mrtasterkhe", password="sinasina!@#", user_type='it_manager'
        )
        self.user = User.objects.create(
            username="ya-adame-alaki", password="sinasina!@#", user_type='user'
        )
        self.fake_college = Faculty.objects.create(name="alaki-hala")
        self.fake_study_field = StudyField.objects.create(
            name="ie-chizi",
            total_units=140,
            level="کارشناسی",
            faculty=self.fake_college,
        )
        self.fake_student = Student.objects.create(
            username="new_student1",
            password="newpassword!@#",
            entry_year=1400,
            entry_term="Mehr",
            seniority=2,
            college=self.fake_college,
            study_field=self.fake_study_field,
            military_status=True,
            user_type='student'
        )

    def test_unauthorized_list_sudent_response_401(self):
        """
        Unauthorized access to students list for users
        """
        url = reverse("users:student-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_forbidden_list_student_response_403(self):
        """
        Forbiddent access to students list for users
        """
        url = reverse("users:student-list")
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_it_manager_list_student_response_200(self):
        """
        Access ITManager to List of a students
        """
        url = reverse("users:student-list")
        self.client.force_authenticate(user=self.it_manager)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_it_manager_create_student_response_201(self):
        """
        Successfull Create a Student by ITManager
        """
        url = reverse("users:student-list")
        data = {
            "username": "new_student",
            "password": "newpassword!@#",
            "verification_password": "newpassword!@#",
            "entry_year": 1400,
            "entry_term": "Mehr",
            "seniority": 2,
            "college": self.fake_college.pk,
            "study_field": self.fake_study_field.pk,
        }
        self.client.force_authenticate(user=self.it_manager)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)

    def test_it_manager_detail_student_response_200(self):
        """
        Access successfully to a student detail data by ITManager
        """
        url = reverse("users:student-detail", kwargs={"pk": self.fake_student.pk})
        self.client.force_authenticate(user=self.it_manager)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_it_manager_detail_student_forbidden_response_403(self):
        """
        Forbidden Access to a student detail data by another users
        """
        url = reverse("users:student-detail", kwargs={"pk": self.fake_student.pk})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_it_manager_detail_student_unauthorized_response_401(self):
        """
        Unauthorized Access to a student detail data without login
        """
        url = reverse("users:student-detail", kwargs={"pk": self.fake_student.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_it_manager_update_student_response_200(self):
        """
        Student Update Successfully by ITManager
        """
        url = reverse("users:student-detail", kwargs={"pk": self.fake_student.pk})

        data = {
            "username": "new_student1",
            "password": "newpassword111",
            "verification_password": "newpassword111",
            "entry_year": 1402,
            "entry_term": "Bahman",
            "seniority": 1,
            "college": self.fake_college.pk,
            "study_field": self.fake_study_field.pk,
        }
        self.client.force_authenticate(user=self.it_manager)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, 200)

    def test_it_manager_delete_student_response_204(self):
        """
        Student Delete Successfully by ITManager
        """
        url = reverse("users:student-detail", kwargs={"pk": self.fake_student.pk})
        self.client.force_authenticate(user=self.it_manager)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)


class TestStudent(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.fake_collage = Faculty.objects.create(name="alaki-hala")
        self.fake_study_field = StudyField.objects.create(
            faculty=self.fake_collage,
            name="ie-chizi",
            total_units=140,
            level="Bachelor",
        )
        self.user = User.objects.create(
            username="ya-adame-alaki", password="sinasina!@#"
        )
        self.fake_deputy_educational = DeputyEducational.objects.create(
            username="us_musa",
            password="sinasina123",
            study_field=self.fake_study_field,
            college=self.fake_collage,
            user_type='deputy_educational',
        )
        self.fake_student = Student.objects.create(
            username="new_student1",
            password="newpassword!@#",
            entry_year=1400,
            entry_term="Mehr",
            seniority=2,
            college=self.fake_collage,
            study_field=self.fake_study_field,
            military_status=True,
            user_type='student'
        )

        self.fake_student2 = Student.objects.create(
            username="new_student2",
            password="newpassword!@#",
            entry_year=1400,
            entry_term="Mehr",
            seniority=2,
            college=self.fake_collage,
            study_field=self.fake_study_field,
            military_status=True,
            user_type='student'
        )

    # Tests for /students/ GET method ---> access by Educational Deputy
    def test_students_list_by_deputy_educational(self):
        """
        Successfull access to students list by Educational Deputy
        """
        url = reverse("users:educational-Deputy-students-list")
        self.client.force_authenticate(user=self.fake_deputy_educational)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_students_list_unauthorized(self):
        """
        Unauthorized Access to students list without Loggin
        """
        url = reverse("users:educational-Deputy-students-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_students_list_forbidden(self):
        """
        Forbidden access with another users
        """
        url = reverse("users:educational-Deputy-students-list")
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    # Tests for /students/{pk}/ GET method ---> access by Educational Deputy and Student
    def test_student_detail_by_owner_student(self):
        """
        Access to student details by Student
        """
        url = reverse(
            "users:educational-Deputy-student-detail",
            kwargs={"pk": self.fake_student.id},
        )
        self.client.force_authenticate(user=self.fake_student)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_student_detail_by_not_owner_student(self):
        """
        Forbidden to student details by another Student
        """
        url = reverse(
            "users:educational-Deputy-student-detail",
            kwargs={"pk": self.fake_student.id},
        )
        self.client.force_authenticate(user=self.fake_student2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_student_detail_by_deputy_educational(self):
        """
        Access to student details by Educational Deputy
        """
        url = reverse(
            "users:educational-Deputy-student-detail",
            kwargs={"pk": self.fake_student.id},
        )
        self.client.force_authenticate(user=self.fake_deputy_educational)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_student_detail_with_no_loggin(self):
        """
        Unauthorized Access to students detail without Loggin
        """
        url = reverse(
            "users:educational-Deputy-student-detail",
            kwargs={"pk": self.fake_student.id},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)


class TestProfessor(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.fake_collage = Faculty.objects.create(name="alaki-hala")
        self.fake_study_field = StudyField.objects.create(
            name="ie-chizi",
            total_units=140,
            level="Bachelor",
            faculty=self.fake_collage,
        )
        self.user = User.objects.create(
            username="ya-adame-alaki", password="sinasina!@#"
        )
        self.fake_deputy_educational = DeputyEducational.objects.create(
            username="us_musa",
            password="sinasina123",
            study_field=self.fake_study_field,
            college=self.fake_collage,
        )
        self.fake_student = Student.objects.create(
            username="new_student1",
            password="newpassword!@#",
            entry_year=1400,
            entry_term="Mehr",
            seniority=2,
            college=self.fake_collage,
            study_field=self.fake_study_field,
            military_status=True,
        )

        self.fake_professor = Professor.objects.create(
            username="agh_moalem",
            password="didichishod123",
            college=self.fake_collage,
            study_field=self.fake_study_field,
            expertise='dummy things',
            rank='2',
        )

        self.fake_professor2 = Professor.objects.create(
            username="ye_agh_moaleme_dige",
            password="didichishod123",
            college=self.fake_collage,
            study_field=self.fake_study_field,
            expertise='dummy things',
            rank='2',
        )

    # Tests for /professors/ GET method ---> access to Professors List by Educational Deputy
    def test_access_to_professors_list_by_deputy_educational(self):
        url = reverse("users:educational-Deputy-professors-list")
        self.client.force_authenticate(user=self.fake_deputy_educational)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_access_to_professors_list_without_loggin(self):
        url = reverse("users:educational-Deputy-professors-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_access_to_professors_list_with_forbidden_user(self):
        url = reverse("users:educational-Deputy-professors-list")
        self.client.force_authenticate(user=self.fake_student)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    # Tests for /professors/{pk} GET method ---> access to Professor detaile by Educational Deputy and professor
    def test_access_to_professor_detail_with_deputy_educational(self):
        url = reverse(
            "users:educational-Deputy-professor-detail",
            kwargs={"pk": self.fake_professor.id},
        )
        self.client.force_authenticate(user=self.fake_deputy_educational)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_access_to_professor_detail_without_loggin(self):
        url = reverse(
            "users:educational-Deputy-professor-detail",
            kwargs={"pk": self.fake_professor.id},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_access_to_professor_detail_with_forbidden_user(self):
        url = reverse(
            "users:educational-Deputy-professor-detail",
            kwargs={"pk": self.fake_professor.id},
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_access_to_professor_detail_with_owner_professor(self):
        url = reverse(
            "users:educational-Deputy-professor-detail",
            kwargs={"pk": self.fake_professor.id},
        )
        self.client.force_authenticate(user=self.fake_professor)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_access_to_professor_detail_with_not_owner_professor(self):
        url = reverse(
            "users:educational-Deputy-professor-detail",
            kwargs={"pk": self.fake_professor.id},
        )
        self.client.force_authenticate(user=self.fake_professor2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
