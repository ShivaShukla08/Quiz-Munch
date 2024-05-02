from django.urls import path
from . import views

urlpatterns = [
    path('home/',views.home, name="home"),
    path('resources/',views.resources, name="resources"),
    path('profile/',views.profile, name="profile"),
    path('notifications/',views.notifications, name="notifications"),
    path('feedback/', views.feedback, name='feedback'),
    path('studentCourseDetail/<str:course_id>/', views.studentCourseDetail, name='studentCourseDetail'),
    path('login/', views.user_login, name="login"),
    path('userlogout/', views.userlogout, name="userlogout"),
    path('quizdisplay/<str:quiz_uuid>/', views.quizdisplay, name='quizdisplay'),
    path('submit_quiz/<str:quiz_uuid>/', views.submit_quiz, name='submit_quiz'),

    path('submit-feedback/', views.submit_feedback, name='submit_feedback'),

]