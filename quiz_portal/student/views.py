from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from .models import StudentsProfile, CoreStream
from . import views                                                   
import math
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from teacher.models import TeacherCourse,TeacherProfile
# Create your views here.

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            print('Username does not exist')

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            print('Username or password is incorrect')
    page = 'login'
    context = {'page':page}
    return render(request,'student/login.html',context)


@login_required
def home(request):
    user_id = request.user.username

    user_details = StudentsProfile.objects.filter(user_id=user_id).first()
    sem = user_details.semester
    stream = user_details.stream
    batch = user_details.batch
 
    course_details = CoreStream.objects.filter(semester=sem, stream=stream).values()
    
    # set myCouses hight in run time
    size =  course_details.count()
    actualheightfcourses = 720
    if(size > 3):   
     actualheightfcourses += (510 * (math.ceil(size/3)-1))

    # get the teacher name & id
    for course in course_details:
        teacher_details = TeacherCourse.objects.filter(course_id=course['course_id'], batch= batch).first()
        # teacher_name = TeacherProfile.objects.filter(id=teacher_details.tid).first()
        # print(teacher_name)
        print(course['course_id'])
        print(course['course_name'])
        print(teacher_details)

    return render(request, 'student/home.html', {"course_details": course_details, "actualheightfcourses": actualheightfcourses})

@login_required
def profile(request):
    user_id = request.user.username
    profile_details = StudentsProfile.objects.filter(user_id=user_id).values()
    return render(request, 'student/profile.html', {"profile_details": profile_details})


def userlogout(request):
    logout(request)
    messages.info(request,'User was logged out')
    return render(request,'student/login.html')
