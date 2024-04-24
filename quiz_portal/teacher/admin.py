from django.contrib import admin

from .models import TeacherProfile,TeacherCourse,Quiz,Quiz_Question_detail,Quiz_details

admin.site.register(TeacherProfile)
admin.site.register(TeacherCourse)
admin.site.register(Quiz_Question_detail)
admin.site.register(Quiz_details)