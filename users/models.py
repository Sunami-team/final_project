import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    personal_number = models.UUIDField(default=uuid.uuid4)  #
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    mobile = models.CharField(max_length=11, null=True, blank=True)
    national_id = models.CharField(max_length=10, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):  #
        return f"{self.first_name} {self.last_name} ({self.username})"


class Student(User):
    entry_year = models.PositiveIntegerField()
    entry_term = models.CharField(max_length=20)
    average = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    college = models.ForeignKey('courses.Faculty', on_delete=models.CASCADE, related_name='students_college')
    study_field = models.ForeignKey('courses.StudyField', on_delete=models.CASCADE, related_name='students_field')
    passed_courses = models.ManyToManyField('courses.Course', related_name='students_passed', blank=True)
    current_courses = models.ManyToManyField('courses.Course', related_name='students_current', blank=True)
    military_status = models.BooleanField()
    seniority = models.PositiveIntegerField()

    def __str__(self):  #
        return f"Student: {self.first_name} {self.last_name} - {self.study_field}"

    class Meta:  #
        verbose_name = "Student"
        verbose_name_plural = "Students"


class ITManager(User):
    pass

    def __str__(self):  #
        return f"IT Manager: {self.first_name} {self.last_name}"

    class Meta:  #
        verbose_name = "IT Manager"
        verbose_name_plural = "IT Managers"


class Professor(User):
    faculty = models.ForeignKey('courses.Faculty', on_delete=models.CASCADE, related_name='professor_faculty')
    study_field = models.ForeignKey('courses.StudyField', on_delete=models.CASCADE, related_name='professor_study')
    expertise = models.DateTimeField()
    rank = models.CharField(max_length=50)

    def __str__(self):  #
        return f"Professor {self.first_name} {self.last_name} - {self.study_field}"

    class Meta:  #
        verbose_name = "Professor"
        verbose_name_plural = "Professors"


class DeputyEducational(User):
    faculty = models.ForeignKey('courses.Faculty', on_delete=models.CASCADE, related_name='deputy_educational_faculty')
    study_field = models.ForeignKey('courses.StudyField', on_delete=models.CASCADE,
                                    related_name='deputy_educational_study')

    def __str__(self):  #
        return f"Deputy for Education: {self.first_name} {self.last_name} - {self.study_field}"

    class Meta:  #
        verbose_name = "Deputy Educational"
        verbose_name_plural = "Deputy Educationals"