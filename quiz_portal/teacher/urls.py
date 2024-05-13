from django.urls import path
from .views import generate_excel
from . import views

urlpatterns = [
    path('home/',views.home, name="teacher_home"),
    path('login/', views.teacher_login, name="teacher_login"),
    path('create_quiz/', views.create_quiz, name="create_quiz"),
    path('delete_quiz/<str:quiz_uuid>/', views.delete_quiz, name='delete_quiz'),

    path('logout/', views.logoutuser, name="logoutuser"),
    path('student_enrol/<str:course_id>/<str:batch>/<str:semester>/', views.student_enrol, name='student_enrol'),
    path('course_detail/<str:course_id>/', views.course_detail, name="course_detail"),
    path('quizquestions/<str:quiz_uuid>/', views.quizquestions, name='quizquestions'),
    path('question_popup/<int:questionNumber>/<str:quiz_uuid>/', views.question_popup, name='question_popup'),
    path('saveChangesQuestion/<str:quiz_uuid>/', views.saveChangesQuestion, name='saveChangesQuestion'),

    path('teacher/', views.teacherprofile, name="teacherprofile"),
    path('upload_quiz/<uuid:course_uuid>/', views.upload_quiz, name='upload_quiz'),
    path('studentresults/<str:quiz_uuid>/', views.studentresults, name='studentresults'),   

    path('generate_excel/<str:quizid>', generate_excel, name='generate_excel'),
 
]

