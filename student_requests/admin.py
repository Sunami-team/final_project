from django.contrib import admin
from .models import *

admin.site.register((CourseRegistrationRequest, CourseCorrectionRequest, GradeReconsiderationRequest, EmergencyDropRequest, TermDropRequest, MilitaryServiceRequest))
