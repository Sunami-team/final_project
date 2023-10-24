import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser



# Create your models here.

class User(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]


    personnel_number = models.UUIDField(default=uuid.uuid4)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    mobile = models.CharField(max_length=11)
    national_id = models.CharField(max_length=10)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    birth_date = models.DateField()


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    entry_year = models.PositiveIntegerField()
    entry_term = models.CharField(max_length=20)
    average = models.DecimalField(max_digits=4, decimal_places=2)
    college = models.ForeignKey('courses.Faculty', on_delete=models.CASCADE, related_name='students_college')
    study_field = models.CharField(max_length=100)
    passed_courses = models.ManyToManyField('courses.Course', related_name='students_passed')
    current_courses = models.ManyToManyField('courses.Course', related_name='students_current')
    military_status = models.BooleanField()
    seniority = models.PositiveIntegerField()

 
class ITManager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
