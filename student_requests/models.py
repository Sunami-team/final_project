from django.db import models


class CourseRegistrationRequest(models.Model):
    student = models.ForeignKey('users.Student', on_delete=models.DO_NOTHING)
    requested_courses = models.ManyToManyField('courses.CourseTerm') 
    approval_status = models.BooleanField(default=False)

    def __str__(self):
        return f"Registration Request by {self.student} - {'Approved' if self.approval_status else 'Pending'}"


class CourseCorrectionRequest(models.Model):
    student = models.ForeignKey('users.Student', on_delete=models.DO_NOTHING)
    courses_to_drop = models.ManyToManyField('courses.CourseTerm', related_name='drop_requests') 
    courses_to_add = models.ManyToManyField('courses.CourseTerm', related_name='add_requests') 
    approval_status = models.BooleanField(default=False)

    def __str__(self):
        return f"Correction Request by {self.student} - {'Approved' if self.approval_status else 'Pending'}"


class GradeReconsiderationRequest(models.Model):
    student = models.ForeignKey('users.Student', on_delete=models.DO_NOTHING)
    course = models.ForeignKey(
        'courses.CourseTerm', on_delete=models.DO_NOTHING)
    reconsideration_text = models.TextField()
    response_text = models.TextField(blank=True)
    approve = models.BooleanField(default=False)

    def __str__(self):
        return f"Grade Reconsideration for {self.course} by {self.student}"


class EmergencyDropRequest(models.Model):
    CHOICES = (  #
        ('pending', 'در انتظار پاسخ'),
        ('approved', 'قبول'),
        ('rejected', 'رد'),
    )
    student = models.ForeignKey('users.Student', on_delete=models.DO_NOTHING)
    course = models.ForeignKey('courses.CourseTerm', on_delete=models.CASCADE)
    result = models.CharField(default='pending', max_length=100, choices=CHOICES)
    student_comment = models.TextField()
    deputy_educational_comment = models.TextField(blank=True)

    def __str__(self):
        return f"Emergency Drop for {self.course} by {self.student} - {'Approved' if self.result else 'Pending'}"

class CourseCorrectionStudentSendToAssistant(models.Model):
    student = models.ForeignKey('users.Student', on_delete=models.DO_NOTHING)
    courses_to_drop = models.ManyToManyField('courses.CourseTerm', related_name='drop_requests_sent_to_assistant', blank=True)
    courses_to_add = models.ManyToManyField('courses.CourseTerm', related_name='add_requests_sent_to_assistant', blank=True)


class TermDropRequest(models.Model):
    RESULT_CHOICES = [
        ('With Seniority', 'With Seniority'),
        ('Without Seniority', 'Without Seniority'),
    ]
    student = models.ForeignKey('users.Student', on_delete=models.DO_NOTHING)
    term = models.ForeignKey('courses.Term', on_delete=models.DO_NOTHING)
    result = models.CharField(max_length=20, choices=RESULT_CHOICES)
    student_comment = models.TextField()
    deputy_educational_comment = models.TextField(blank=True)

    def __str__(self):
        return f"Term Drop for {self.term} by {self.student} - Result: {self.result}"


class CourseCorrectionStudentRequest(models.Model):
    student = models.ForeignKey('users.Student', on_delete=models.DO_NOTHING)
    courses_to_drop = models.ManyToManyField('courses.CourseTerm', related_name='drop_requests', blank=True)
    courses_to_add = models.ManyToManyField('courses.CourseTerm', related_name='add_requests', blank=True)
    approval_status = models.BooleanField(default=False)

class MilitaryServiceRequest(models.Model):
    student = models.ForeignKey('users.Student', on_delete=models.DO_NOTHING)
    term = models.ForeignKey('courses.Term', on_delete=models.DO_NOTHING)
    proof_document = models.FileField(upload_to='military_docs/')
    issuance_place = models.CharField(max_length=100)

    def __str__(self):
        return f"Military Service Request for {self.term} by {self.student} - Issuance Place: {self.issuance_place}"


