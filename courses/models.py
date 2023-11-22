from django.db import models


class Faculty(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Course(models.Model):
    COURSE_TYPE_CHOICES = [
        ("B", "پایه"),
        ("G", "عمومی"),
        ("P", "تخصصی"),
        ("O", "اختیاری"),
    ]

    college = models.ForeignKey(
        Faculty, on_delete=models.CASCADE, related_name="courses"
    )
    name = models.CharField(max_length=255)
    course_unit = models.PositiveIntegerField(default=3)
    course_type = models.CharField(max_length=1, choices=COURSE_TYPE_CHOICES)

    def __str__(self):
        return self.name


class CourseRequistes(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    pre_requisites = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="courses_required"
    )
    co_requisites = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="courses_concurrent"
    )


class Term(models.Model):
    pre_GPA_term = models.DecimalField(
        max_digits=4, decimal_places=2, default=0
    )  # previous grade point average
    name = models.CharField(max_length=100)
    start_course_selection = models.DateField()
    end_course_selection = models.DateField()
    start_classes = models.DateField()
    end_classes = models.DateField()
    start_course_correction = models.DateField()
    end_course_correction = models.DateField()
    end_emergency_drop = models.DateField()
    start_exams = models.DateField()
    end_term = models.DateField()

    def __str__(self):
        return f"{self.id} --> {self.name} --> {self.start_classes.year}"


class CourseTerm(models.Model):
    DAYS_CHOICES = [
        ("Mon", "دوشنبه"),
        ("Tue", "سه‌شنبه"),
        ("Wed", "چهارشنبه"),
        ("Thu", "پنج‌شنبه"),
        ("Fri", "جمعه"),
        ("Sat", "شنبه"),
        ("Sun", "یک‌شنبه"),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    professor = models.ForeignKey("users.Professor", on_delete=models.CASCADE)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    class_day = models.CharField(max_length=3, choices=DAYS_CHOICES, default="Sat")
    class_time = models.TimeField(default="8:00:00")
    exam_date_time = models.DateTimeField()
    class_location = models.CharField(max_length=255, blank=True)
    exam_location = models.CharField(max_length=255, blank=True)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.course.name} --> Professor:{self.professor.first_name}"


class StudentCourse(models.Model):
    COURSE_STATUS_CHOICES = [
        ("pass", "قبول"),
        ("failed", "مردود"),
        ("idk", "مشروط"),
    ]
    student = models.ForeignKey("users.Student", on_delete=models.CASCADE)
    course_term = models.ForeignKey(
        'courses.Course', on_delete=models.CASCADE, related_name='student_course')
    real_course_term = models.ForeignKey(
        'courses.CourseTerm', on_delete=models.CASCADE, related_name='student_courseterm')
    term = models.ForeignKey('courses.Term', on_delete=models.CASCADE)

    course_status = models.CharField(
        max_length=10, blank=True, choices=COURSE_STATUS_CHOICES
    )
    grade = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.student.first_name} {self.student.last_name} --> {self.course_term.name}"


class TermStudentProfessor(models.Model):
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    students = models.ForeignKey("users.Student", on_delete=models.CASCADE)
    professors = models.ForeignKey("users.Professor", on_delete=models.CASCADE)


class StudyField(models.Model):
    LEVEL_CHOICES = [
        ("Bachelor", "کارشناسی"),
        ("Master", "کارشناسی ارشد"),
        ("PHD", "دکتری"),
    ]

    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    educations_groupe = models.CharField(max_length=255, blank=True)
    total_units = models.PositiveIntegerField()
    level = models.CharField(max_length=255, choices=LEVEL_CHOICES)

    def __str__(self):
        return self.name
