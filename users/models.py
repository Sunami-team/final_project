import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser



# Create your models here.

class User(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]


    personnel_number = models.UUIDField(default=uuid.uuid4, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    mobile = models.CharField(max_length=11, null=True, blank=True)
    national_id = models.CharField(max_length=10, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)


class Student(User):
    entry_year = models.PositiveIntegerField()
    entry_term = models.CharField(max_length=20)
    average = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    college = models.ForeignKey('courses.Faculty', on_delete=models.CASCADE, related_name='students_college')
    study_field = models.ForeignKey('courses.StudyField', on_delete=models.CASCADE, related_name='students_field')
    passed_courses = models.ManyToManyField('courses.Course', related_name='students_passed')
    current_courses = models.ManyToManyField('courses.Course', related_name='students_current')
    military_status = models.BooleanField()
    seniority = models.PositiveIntegerField()

 
class ITManager(User):
    pass


class Professor(User):
    faculty = models.ForeignKey('courses.Faculty', on_delete=models.CASCADE, related_name='professor_faculty')
    study_field = models.ForeignKey('courses.StudyField', on_delete=models.CASCADE, related_name='professor_study')
    expertise = models.DateTimeField()
    rank = models.CharField()


class DeputyEducational(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    faculty = models.ForeignKey('courses.Faculty', on_delete=models.CASCADE, related_name='deputy_educational_faculty')
    study_field = models.ForeignKey('courses.StudyField', on_delete=models.CASCADE, related_name='deputy_educational_study')

