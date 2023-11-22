from django.db import models


class CourseRegistrationRequest(models.Model):
    student = models.ForeignKey("users.Student", on_delete=models.CASCADE)
    requested_courses = models.ManyToManyField(
        "courses.CourseTerm", related_name="course_registration_request"
    )
    # requested_courses = models.ManyToManyField('courses.CourseTerm') #### get from StudentCourse ####
    approval_status = models.BooleanField(default=False)
    adviser_professor = models.ForeignKey("users.professor",null=True,blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"Registration Request by {self.student} - {'Approved' if self.approval_status else 'Pending'}"


class CourseCorrectionRequest(models.Model):
    student = models.ForeignKey("users.Student", on_delete=models.CASCADE)
    courses_to_drop = models.ManyToManyField(
        "courses.CourseTerm", related_name="drop_requests_course_correction"
    )
    courses_to_add = models.ManyToManyField(
        "courses.CourseTerm", related_name="add_requests_course_correction"
    )
    # courses_to_drop = models.ManyToManyField('courses.CourseTerm', related_name='drop_requests') #### get from StudentCourse ####
    # courses_to_add = models.ManyToManyField('courses.CourseTerm', related_name='add_requests') #### get from StudentCourse ####
    approval_status = models.BooleanField(default=False)

    def __str__(self):
        return f"Correction Request by {self.student} - {'Approved' if self.approval_status else 'Pending'}"


class GradeReconsiderationRequest(models.Model):
    student = models.ForeignKey("users.Student", on_delete=models.CASCADE)
    course = models.ForeignKey("courses.CourseTerm", on_delete=models.CASCADE)
    reconsideration_text = models.TextField()
    response_text = models.TextField(blank=True)

    def __str__(self):
        return f"Grade Reconsideration for {self.course} by {self.student}"


class EmergencyDropRequest(models.Model):
    CHOICES = (  #
        ("pending", "در انتظار پاسخ"),
        ("approved", "قبول"),
        ("rejected", "رد"),
    )
    student = models.ForeignKey("users.Student", on_delete=models.CASCADE)
    course = models.ForeignKey("courses.CourseTerm", on_delete=models.CASCADE)
    result = models.CharField(default="pending", max_length=100, choices=CHOICES)
    # course = models.ForeignKey(
    #     'courses.StudentCourse', on_delete=models.DO_NOTHING)
    result = models.BooleanField(default=False)
    student_comment = models.TextField()
    deputy_educational_comment = models.TextField(blank=True)

    def __str__(self):
        return f"Emergency Drop for {self.course} by {self.student} - {'Approved' if self.result else 'Pending'}"


class CourseSelectionStudentSendToAssistant(models.Model):
    student = models.ForeignKey("users.Student", on_delete=models.CASCADE)
    courses_to_drop = models.ManyToManyField(
        "courses.CourseTerm",
        related_name="selection_student_send_to_assistant_drop",
        blank=True,
    )
    courses_to_add = models.ManyToManyField(
        "courses.CourseTerm",
        related_name="selection_student_send_to_assistant_add",
        blank=True,
    )


class CourseCorrectionStudentSendToAssistant(models.Model):
    student = models.ForeignKey("users.Student", on_delete=models.CASCADE)
    courses_to_drop = models.ManyToManyField(
        "courses.CourseTerm",
        related_name="correction_student_send_to_assistant_drop",
        blank=True,
    )
    courses_to_add = models.ManyToManyField(
        "courses.CourseTerm",
        related_name="correction_student_send_to_assistant_add",
        blank=True,
    )


class TermDropRequest(models.Model):
    RESULT_CHOICES = [
        ("With Seniority", "With Seniority"),
        ("Without Seniority", "Without Seniority"),
    ]
    student = models.ForeignKey("users.Student", on_delete=models.CASCADE)
    term = models.ForeignKey("courses.Term", on_delete=models.CASCADE)
    result = models.CharField(max_length=20, choices=RESULT_CHOICES)
    student_comment = models.TextField()
    deputy_educational_comment = models.TextField(blank=True)

    def __str__(self):
        return f"Term Drop for {self.term} by {self.student} - Result: {self.result}"


class CourseCorrectionStudentRequest(models.Model):
    student = models.ForeignKey("users.Student", on_delete=models.CASCADE)
    courses_to_drop = models.ManyToManyField(
        "courses.CourseTerm",
        related_name="correction_student_requests_to_drop",
        blank=True,
    )
    courses_to_add = models.ManyToManyField(
        "courses.CourseTerm",
        related_name="correction_student_requests_to_add",
        blank=True,
    )
    approval_status = models.BooleanField(default=False)


class CourseSelectionStudentRequest(models.Model):
    student = models.ForeignKey("users.Student", on_delete=models.CASCADE)
    courses_to_drop = models.ManyToManyField(
        "courses.CourseTerm",
        related_name="selection_student_requests_to_drop",
        blank=True,
    )
    courses_to_add = models.ManyToManyField(
        "courses.CourseTerm",
        related_name="selection_student_requests_to_add",
        blank=True,
    )
    approval_status = models.BooleanField(default=False)


class MilitaryServiceRequest(models.Model):
    student = models.ForeignKey("users.Student", on_delete=models.CASCADE)
    # deputy_educational = models.ForeignKey("users.DeputyEducational", on_delete=models.CASCADE)
    term = models.ForeignKey("courses.Term", on_delete=models.CASCADE)
    proof_document = models.FileField(upload_to="military_docs/")
    issuance_place = models.CharField(max_length=100)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"Military Service Request for {self.term} by {self.student} - Issuance Place: {self.issuance_place}"
