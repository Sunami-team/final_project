import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import timezone, timedelta
from config.minio_storage import minio_client


class User(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    USER_TYPE_CHOICES = [
        ('student', 'Student'),
        ('professor', 'Professor'),
        ('it_manager', 'IT Manager'),
        ('deputy_educational', 'Deputy Educational'),
    ]

    personal_number = models.UUIDField(default=uuid.uuid4)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    mobile = models.CharField(max_length=11, blank=True)
    national_id = models.CharField(max_length=10, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default='student',
    )


    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"


class ChangePasswordToken(models.Model):

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return self.created_at < timezone.now() - timedelta(minutes=5)


class Student(User):
    entry_year = models.PositiveIntegerField()
    entry_term = models.CharField(max_length=20)
    average = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, blank=True)
    college = models.ForeignKey(
        'courses.Faculty', on_delete=models.DO_NOTHING, related_name='students_college')
    study_field = models.ForeignKey(
        'courses.StudyField', on_delete=models.DO_NOTHING, related_name='students_field')
    military_status = models.BooleanField()
    seniority = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class ITManager(User):
    class Meta:
        verbose_name = "IT Manager"
        verbose_name_plural = "IT Managers"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Professor(User):
    RANK_CHOICES = [
        ('1', 'مربی'),
        ('2', 'استادیار'),
        ('3', 'دانشیار'),
        ('4', 'استاد'),
    ]
    college = models.ForeignKey(
        'courses.Faculty', on_delete=models.DO_NOTHING, related_name='professor_faculty')
    study_field = models.ForeignKey(
        'courses.StudyField', on_delete=models.DO_NOTHING, related_name='professor_study')
    expertise = models.TextField()
    rank = models.CharField(max_length=1, choices=RANK_CHOICES, default='1')

    class Meta:
        verbose_name = "Professor"
        verbose_name_plural = "Professors"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class DeputyEducational(User):
    college = models.ForeignKey(
        'courses.Faculty', on_delete=models.DO_NOTHING, related_name='deputy_educational_faculty')
    study_field = models.ForeignKey('courses.StudyField', on_delete=models.DO_NOTHING,
                                    related_name='deputy_educational_study')

    class Meta:
        verbose_name = "Deputy Educational"
        verbose_name_plural = "Deputy Educationals"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
