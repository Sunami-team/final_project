from django.db import models
# from courses.models import *
# from users.models import *



class CourseRegistrationRequest(models.Model):
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE)
    requested_courses = models.ManyToManyField('courses.CourseTerm')
    approval_status = models.BooleanField(default=False)


class CourseCorrectionRequest(models.Model):
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE)
    courses_to_drop = models.ManyToManyField('courses.CourseTerm', related_name='drop_requests')
    courses_to_add = models.ManyToManyField('courses.CourseTerm', related_name='add_requests')
    approval_status = models.BooleanField(default=False)


class GradeReconsiderationRequest(models.Model):
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE)
    course = models.ForeignKey('courses.CourseTerm', on_delete=models.CASCADE)
    reconsideration_text = models.TextField()
    response_text = models.TextField(blank=True, null=True)


class EmergencyDropRequest(models.Model):
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE)
    course = models.ForeignKey('courses.CourseTerm', on_delete=models.CASCADE)
    result = models.BooleanField(default=False)
    student_comment = models.TextField()
    deputy_educational_comment = models.TextField(blank=True, null=True)


class TermDropRequest(models.Model):
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE)
    term = models.ForeignKey('courses.Term', on_delete=models.CASCADE)
    result = models.CharField(max_length=50, choices=[('With Seniority', 'With Seniority'),
                                                      ('Without Seniority', 'Without Seniority')])
    student_comment = models.TextField()
    deputy_educational_comment = models.TextField(blank=True, null=True)


class MilitaryServiceRequest(models.Model):
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE)
    proof_document = models.FileField(upload_to='military_docs/')
    term = models.ForeignKey('courses.Term', on_delete=models.CASCADE)
    issuance_place = models.CharField(max_length=100)
