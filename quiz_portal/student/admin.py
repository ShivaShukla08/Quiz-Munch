from django.contrib import admin

from .models import StudentProfile,CoreStream, StudentsProfile

admin.site.register(CoreStream)
admin.site.register(StudentsProfile)