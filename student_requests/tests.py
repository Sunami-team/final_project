from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from users.models import DeputyEducational, User, Student
from courses.models import Faculty, StudyField, Term
from student_requests.models import TermDropRequest
from users.models import Professor
from datetime import datetime, date
# Create your tests here.

class TestDropTerm(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='ya-adame-alaki', password='sinasina!@#')
        self.fake_collage = Faculty.objects.create(name='alaki-hala')
        self.fake_study_field = StudyField.objects.create(name='ie-chizi', total_units=140, level='کارشناسی')
        self.fake_deputy_educational = DeputyEducational.objects.create(username='us_musa', password='sinasina123',
                                                                        faculty=self.fake_collage, study_field=self.fake_study_field)
        self.fake_student = Student.objects.create(username='new_student1',
            password='newpassword!@#',
            entry_year= 1400,
            entry_term='Mehr',
            seniority=3,
            college=self.fake_collage,
            study_field=self.fake_study_field,
            military_status=True
            )
        
                
        self.fake_professor = Professor.objects.create(
            username='agh_moalem',
            password='didichishod123',
            faculty=self.fake_collage,
            study_field=self.fake_study_field,
            expertise=datetime.now(),
            rank='OstatTamam'
        )

        self.fake_term = Term.objects.create(
            name = 'Mehr',
            # students = self.fake_student,
            # professors = self.fake_professor,
            start_course_selection = date(year=2023, month=6, day=1),
            end_course_selection = date(year=2023, month=6, day=15),
            start_classes = date(year=2023, month=6, day=16),
            end_classes = date(year=2023, month=10, day=15),
            start_course_correction = date(year=2023, month=6, day=15),
            end_course_correction = date(year=2023, month=6, day=30),
            end_emergency_drop = date(year=2023, month=6, day=30),
            start_exams = date(year=2023, month=10, day=16),
            end_term = date(year=2023, month=10, day=30),
        )
        self.fake_term.students.add(self.fake_student)
        self.fake_term.professors.add(self.fake_professor)
        self.fake_term.save()

        self.fake_drop_request = TermDropRequest.objects.create(
            student = self.fake_student,
            term=self.fake_term,
            result ='With Seniority',
            student_comment='NoThing',
            deputy_educational_comment='NoThing',
        )
        # self.fake_drop_request.student.set(self.fake_student)
    def test_drop_term_request_list_response_200(self):
        url = reverse('student_requests:remove-term-list')
        self.client.force_authenticate(self.fake_deputy_educational)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_drop_term_request_list_unauthorization(self):
        url = reverse('student_requests:remove-term-list')
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
    
    def test_drop_term_request_detail_response_200(self):
        url = reverse('student_requests:remove-term-detail', kwargs={'pk':self.fake_student.id})
        self.client.force_authenticate(self.fake_deputy_educational)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_drop_term_request_detail_response_403(self):
        url = reverse('student_requests:remove-term-detail', kwargs={'pk':self.fake_student.id})
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
    
    def test_drop_test_drop_term_request_detail_post_response_200(self):
        url = reverse('student_requests:remove-term-detail', kwargs={'pk':self.fake_student.id})
        self.client.force_authenticate(self.fake_deputy_educational)
        data = {
            'deputy_educational_comment':'Koo Koo Sabzi',
            'accept': True
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, 200)