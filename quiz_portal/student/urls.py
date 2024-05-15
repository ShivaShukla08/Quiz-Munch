from django.urls import path
from . import views

urlpatterns = [
    path('home/',views.home, name="home"),
    path('resources/',views.resources, name="resources"),
    path('profile/',views.profile, name="profile"),
    path('notifications/',views.notifications, name="notifications"),
    path('feedback/', views.feedback, name='feedback'),
    path('help/', views.help, name='help'),
    path('quiz-details/<str:course_id>/', views.studentCourseDetail, name='studentCourseDetail'),
    path('login/', views.user_login, name="login"),
    path('logout/', views.userlogout, name="userlogout"),
    path('quiz-display/<str:quiz_uuid>/', views.quizdisplay, name='quizdisplay'),
    path('submit-quiz/<str:quiz_uuid>/', views.submit_quiz, name='submit_quiz'),
    path('quiz-result/<str:quiz_uuid>/', views.Quizresult, name="Quizresult"),
    path('question/<int:questionNumber>/<str:quiz_uuid>/', views.ViewQuizQues, name='ViewQuizQues'),
    path('verify.certificate/<str:certificated_id>/', views.quizCertificated, name="quizCertificated"),
    path('submit-feedback/', views.submit_feedback, name='submit_feedback'),
]