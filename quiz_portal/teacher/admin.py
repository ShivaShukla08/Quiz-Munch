from django.contrib import admin

from .models import TeacherProfile,TeacherCourse,Quiz,QuizQuestion

admin.site.register(TeacherProfile)
admin.site.register(TeacherCourse)
admin.site.register(Quiz)
admin.site.register(QuizQuestion)
