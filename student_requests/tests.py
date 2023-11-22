from django.test import TestCase
from rest_framework.test import APIClient
from users.models import User, DeputyEducational, Student, Professor
from courses.models import Faculty, StudyField, Term
from student_requests.models import TermDropRequest, GradeReconsiderationRequest
from courses.models import Course, CourseTerm, Faculty
from django.urls import reverse
from datetime import datetime, date

# Create your tests here.


class TestDropTerm(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            username="ya-adame-alaki", password="sinasina!@#"
        )
        self.fake_collage = Faculty.objects.create(name="alaki-hala")
        self.fake_study_field = StudyField.objects.create(
            name="ie-chizi",
            total_units=140,
            level="کارشناسی",
            faculty=self.fake_collage,
        )
        self.fake_deputy_educational = DeputyEducational.objects.create(
            username="us_musa",
            password="sinasina123",
            college=self.fake_collage,
            study_field=self.fake_study_field,
            user_type='deputy_educational'
        )
        self.fake_student = Student.objects.create(
            username="new_student1",
            password="newpassword!@#",
            entry_year=1400,
            entry_term="Mehr",
            seniority=3,
            college=self.fake_collage,
            study_field=self.fake_study_field,
            military_status=True,
            email="sinahs1992@gmail.com",
            first_name="sina",
            last_name="hosseini",
            user_type="student",
        )

        self.fake_professor = Professor.objects.create(
            username="agh_moalem",
            password="didichishod123",
            college=self.fake_collage,
            study_field=self.fake_study_field,
            expertise=datetime.now(),
            rank="OstatTamam",
            user_type='professor'
        )

        self.fake_term = Term.objects.create(
            name="Mehr",
            start_course_selection=date(year=2023, month=6, day=1),
            end_course_selection=date(year=2023, month=6, day=15),
            start_classes=date(year=2023, month=6, day=16),
            end_classes=date(year=2023, month=10, day=15),
            start_course_correction=date(year=2023, month=6, day=15),
            end_course_correction=date(year=2023, month=6, day=30),
            end_emergency_drop=date(year=2023, month=6, day=30),
            start_exams=date(year=2023, month=10, day=16),
            end_term=date(year=2023, month=10, day=30),
        )
        self.fake_term.save()

        self.fake_drop_request = TermDropRequest.objects.create(
            student=self.fake_student,
            term=self.fake_term,
            result="With Seniority",
            student_comment="NoThing",
            deputy_educational_comment="NoThing",
        )
        # self.fake_drop_request.student.set(self.fake_student)

    def test_drop_term_request_list_response_200(self):
        url = reverse("student_requests:remove-term-list")
        self.client.force_authenticate(self.fake_deputy_educational)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_drop_term_request_list_unauthorization(self):
        url = reverse("student_requests:remove-term-list")
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_drop_term_request_detail_response_200(self):
        url = reverse(
            "student_requests:remove-term-detail",
            kwargs={"student_id": self.fake_student.pk, "term_id": self.fake_term.pk},
        )

        self.client.force_authenticate(self.fake_deputy_educational)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_drop_term_request_detail_response_403(self):
        url = reverse(
            "student_requests:remove-term-detail",
            kwargs={"student_id": self.fake_student.id, "term_id": self.fake_term.id},
        )
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_drop_test_drop_term_request_detail_post_response_200(self):
        url = reverse(
            "student_requests:remove-term-detail",
            kwargs={"student_id": self.fake_student.id, "term_id": self.fake_term.id},
        )
        self.client.force_authenticate(self.fake_deputy_educational)
        data = {"deputy_educational_comment": "Koo Koo Sabzi", "accept": True}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, 200)


# /assistant/{pk,me}/courses/{c-pk}/prof-approved/{pk}/ GET, PUT
class TestAssistantGradeCorrection(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            username="ya-adame-alaki", password="sinasina!@#"
        )
        self.fake_collage = Faculty.objects.create(name="alaki-hala")
        self.fake_study_field = StudyField.objects.create(
            name="ie-chizi",
            total_units=140,
            level="Bachelor",
            faculty=self.fake_collage,
        )

        self.fake_student = Student.objects.create(
            username="new_student1",
            password="newpassword!@#",
            entry_year=1400,
            entry_term="Mehr",
            seniority=3,
            college=self.fake_collage,
            study_field=self.fake_study_field,
            military_status=True,
            user_type='student',
        )

        self.fake_professor = Professor.objects.create(
            username="agh_moalem",
            password="didichishod123",
            college=self.fake_collage,
            study_field=self.fake_study_field,
            expertise='dummy',
            rank="2",
            user_type='professor',
        )
        self.fake_course = Course.objects.create(
            name="Math", course_type="G", college=self.fake_collage
        )
        self.fake_term = Term.objects.create(
            name="Mehr",
            pre_GPA_term=15,
            start_course_selection=date(year=2023, month=6, day=1),
            end_course_selection=date(year=2023, month=6, day=15),
            start_classes=date(year=2023, month=6, day=16),
            end_classes=date(year=2023, month=10, day=15),
            start_course_correction=date(year=2023, month=6, day=15),
            end_course_correction=date(year=2023, month=6, day=30),
            end_emergency_drop=date(year=2023, month=6, day=30),
            start_exams=date(year=2023, month=10, day=16),
            end_term=date(year=2023, month=10, day=30),
        )

        self.fake_courese_term = CourseTerm.objects.create(
            course=self.fake_course,
            exam_date_time=datetime.now(),
            professor=self.fake_professor,
            capacity=40,
            term=self.fake_term,
        )
        self.fake_grade_reconsider = GradeReconsiderationRequest.objects.create(
            student=self.fake_student,
            course=self.fake_courese_term,
            reconsideration_text="Ma eeteraz darim",
        )

        self.fake_deputy_educational = DeputyEducational.objects.create(
            username="us_musa",
            password="sinasina123",
            college=self.fake_collage,
            study_field=self.fake_study_field,
            user_type='deputy_educational'
        )

    def test_assistant_grade_correction_list_status_200(self):
        url = reverse(
            "student_requests:assistant-change-grade-list",
            kwargs={
                "professor_id": self.fake_professor.id,
                "course_id": self.fake_courese_term.id,
            },
        )
        self.client.force_authenticate(user=self.fake_deputy_educational)
        response = self.client.get(url)
        print('ZERNAZAN', response.context)
        self.assertEqual(response.status_code, 200)

    def test_assistant_grade_correction_list_status_forbidden_403(self):
        url = reverse(
            "student_requests:assistant-change-grade-list",
            kwargs={
                "professor_id": self.fake_professor.id,
                "course_id": self.fake_courese_term.id,
            },
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_assistant_grade_correction_student_detail_status_200(self):
        url = reverse(
            "student_requests:assistant-change-grade-list-student-detail",
            kwargs={
                "professor_id": self.fake_professor.id,
                "course_id": self.fake_courese_term.id,
                "student_id": self.fake_student.id,
            },
        )
        self.client.force_authenticate(user=self.fake_deputy_educational)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_assistant_grade_correction_student_detail_forbidden_status_403(self):
        url = reverse(
            "student_requests:assistant-change-grade-list-student-detail",
            kwargs={
                "professor_id": self.fake_professor.id,
                "course_id": self.fake_courese_term.id,
                "student_id": self.fake_student.id,
            },
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_assistant_grade_correction_student_put_200(self):
        url = reverse(
            "student_requests:assistant-change-grade-list-student-detail",
            kwargs={
                "professor_id": self.fake_professor.id,
                "course_id": self.fake_courese_term.id,
                "student_id": self.fake_student.id,
            },
        )
        self.client.force_authenticate(user=self.fake_deputy_educational)
        data = {"response_text": "Some text from Educational Deputy", "approve": True}
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, 200)
