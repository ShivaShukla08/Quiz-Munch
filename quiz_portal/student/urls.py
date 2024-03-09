from django.urls import path
from . import views

urlpatterns = [
    path('',views.profiles, name="profile"),
    path('loginstudent/', views.loginstudent, name="loginstudent"),
]