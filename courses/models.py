from django.db import models

course_type_choices = [('G', 'عمومی'), ('P', 'تخصصی')]


class Course(models.Model):
    name = models.CharField(max_length=255)
    faculty = models.ManyToManyField('courses.Faculty')
    pre_requisites = models.ManyToManyField('courses.Course', related_name='courses_required', null=True, blank=True)
    co_requisites = models.ManyToManyField('courses.Course', related_name='courses_concurrent', null=True, blank=True)
    course_unit = models.PositiveIntegerField()
    course_type = models.CharField(max_length=255, choices=course_type_choices)

    def __str__(self):
        return self.name


week_days = [('M', 'Monday'), ('T', 'Tuesday'), ('W', 'Wednesday'),
             ('T', 'Thursday'), ('F', 'Friday'), ('Sat', 'Saturday'), ('Sun', 'Sunday')]


class CourseTerm(models.Model):
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)
    class_day = models.CharField(max_length=100, choices=week_days)
    class_time = models.TimeField()
    exam_date_time = models.DateTimeField()
    class_location = models.CharField(max_length=255)
    exam_location = models.CharField(max_length=255)
    professor = models.ForeignKey('users.Professor', on_delete=models.DO_NOTHING, blank=True, null=True)
    capacity = models.PositiveIntegerField()
    term = models.ForeignKey('courses.Term', on_delete=models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return f"{self.course.name} --> Professor:{self.professor.first_name}"


status_choices = [('pass', 'قبول'), ('failed', 'مردود'), ('idk', 'مشروط')]


class StudentCourse(models.Model):
    student = models.ForeignKey('users.Student', on_delete=models.SET_NULL, null=True, blank=True)
    course_term = models.ForeignKey('courses.CourseTerm', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True, choices=status_choices)
    grade = models.FloatField(max_length=255, null=True, blank=True)
    term = models.ForeignKey('courses.Term', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.student.first_name} {self.student.last_name} --> {self.course_term.course.name}"


class Term(models.Model):
    name = models.CharField(max_length=255, choices=[('Mehr', 'مهر'), ('Bahman', 'بهمن'), ('Summer', 'تابستان')])
    students = models.ManyToManyField('users.Student')
    professors = models.ManyToManyField('users.Professor')
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
        return f"{self.name} --> {self.start_classes.year}"


class Faculty(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class StudyField(models.Model):
    name = models.CharField(max_length=255)  # Choice field
    educations_groupe = models.CharField(max_length=255)  # Choice field
    faculty = models.ManyToManyField('courses.Faculty')
    total_units = models.PositiveIntegerField()
    level = models.CharField(max_length=255,
                             choices=[('کارشناسی', 'کارشناسی'), ('کارشناسی ارشد', 'کارشناسی ارشد'), ('PHD', 'PHD')])
