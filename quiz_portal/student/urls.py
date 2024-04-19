from django.urls import path
from . import views

urlpatterns = [
    path('home/',views.home, name="home"),
    path('profile/',views.profile, name="profile"),
    path('login/', views.user_login, name="login"),
    path('userlogout/', views.userlogout, name="userlogout"),
]
