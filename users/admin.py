from django.contrib import admin

from django.contrib import admin
from .models import User, Professor, Student, ITManager, DeputyEducational

admin.site.register(User)
admin.site.register(Professor)
admin.site.register(Student)
admin.site.register(ITManager)
admin.site.register(DeputyEducational)

