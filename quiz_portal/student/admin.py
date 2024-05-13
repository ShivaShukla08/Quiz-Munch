from django.contrib import admin

from .models import StudentProfile,CoreStreams, StudentsProfile,response_table, Feedback, QuizDetailsResponse, CompletionCertificates

admin.site.register(CoreStreams)
admin.site.register(StudentsProfile)
admin.site.register(response_table)
admin.site.register(Feedback)
admin.site.register(QuizDetailsResponse)
admin.site.register(CompletionCertificates)