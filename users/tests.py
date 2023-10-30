from django.test import TestCase
from django.urls import reverse
from .models import ITManager, User, Student
from rest_framework.test import APIClient
from courses.models import Faculty, StudyField


class TestAdminStudentApi(TestCase):
    """This is test class is for Create, List, Retieve, Update, Delete a student By ITManager"""
    def setUp(self):
        self.client = APIClient()
        self.it_manager = ITManager.objects.create(username='mrtaster', password='sinasina!@#')
        self.user = User.objects.create(username='ya-adame-alaki', password='sinasina!@#')
        self.fake_collage = Faculty.objects.create(name='alaki-hala')
        self.fake_study_field = StudyField.objects.create(name='ie-chizi', total_units=140, level='کارشناسی')
        self.fake_student = Student.objects.create(username='new_student1',
            password='newpassword!@#',
            entry_year= 1400,
            entry_term='Mehr',
            seniority=2,
            college=self.fake_collage,
            study_field=self.fake_study_field,
            military_status=True
            )
        
    def test_unauthorized_list_sudent_response_401(self):
        """
        Unauthorized access to students list for users
        """
        url = reverse('users:student-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)


    def test_forbidden_list_student_response_403(self):
        """
        Forbiddent access to students list for users
        """
        url = reverse('users:student-list')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)


    def test_it_manager_list_student_response_200(self):
        """
        Access ITManager to List of a students
        """
        url = reverse('users:student-list')
        self.client.force_authenticate(user=self.it_manager)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


    def test_it_manager_create_student_response_201(self):
        """
        Successfull Create a Student by ITManager
        """
        url = reverse('users:student-list')
        data = {
            'username' : 'new_student',
            'password' : 'newpassword!@#',
            'verification_password' : 'newpassword!@#',
            'entry_year' : 1400,
            'entry_term' : 'Mehr',
            'seniority' : 2,
            'college' : self.fake_collage.pk,
            'study_field' : self.fake_study_field.pk
        }
        self.client.force_authenticate(user=self.it_manager)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)


    def test_it_manager_detail_student_response_200(self):
        """
        Access successfully to a student detail data by ITManager
        """
        url = reverse('users:student-detail', kwargs={'pk': self.fake_student.pk})
        self.client.force_authenticate(user=self.it_manager)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


    def test_it_manager_detail_student_forbidden_response_403(self):
        """
        Forbidden Access to a student detail data by another users
        """
        url = reverse('users:student-detail', kwargs={'pk': self.fake_student.pk})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
    
    def test_it_manager_detail_student_unauthorized_response_401(self):
        """
        Unauthorized Access to a student detail data without login
        """
        url = reverse('users:student-detail', kwargs={'pk': self.fake_student.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    
    def test_it_manager_update_student_response_200(self):
        """
        Student Update Successfully by ITManager
        """
        url = reverse('users:student-detail', kwargs={'pk': self.fake_student.pk})

        data = {
            'username' : 'new_student1',
            'password' : 'newpassword111',
            'verification_password' : 'newpassword111',
            'entry_year' : 1402,
            'entry_term' : 'Bahman',
            'seniority' : 1,
            'college' : self.fake_collage.pk,
            'study_field' : self.fake_study_field.pk
        }
        self.client.force_authenticate(user=self.it_manager)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, 200)


    def test_it_manager_delete_student_response_204(self):
        """
        Student Delete Successfully by ITManager
        """
        url = reverse('users:student-detail', kwargs={'pk': self.fake_student.pk})
        self.client.force_authenticate(user=self.it_manager)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
