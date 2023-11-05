from django.contrib import admin
from .models import CorrectionTemporaryRequests, TermDropRequest
# Register your models here.

admin.site.register(CorrectionTemporaryRequests)
admin.site.register(TermDropRequest)