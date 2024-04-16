from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
import json
from django.http import HttpResponse
from .forms import QuizForm
from .models import TeacherProfile,TeacherCourse,Quiz,QuizQuestion
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def profiles(request):
    return render(request, 'teacher/profile.html')

def teacher_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            print('Username does not exist')

        user = authenticate(request,username=username,password=password)

        if user is not None:
            id = username
            login(request, user)
            # print(2222)
            return redirect('teacher_home')
        else:
            print('Username or password is incorrect')
    page = 'login'
    context = {'page':page}
    return render(request,'teacher/login.html',context)

def logoutuser(request):
    logout(request)
    messages.info(request,'User was logged out')
    return redirect('teacher_login')

@login_required
def home(request):
    user_id = request.user.username
    details = TeacherCourse.objects.filter(tid=user_id)
    print(user_id)
    return render(request, 'teacher/home.html', {'details': details})


def course_detail(request,course_id):
    return render(request, 'teacher/course_detail.html')

@login_required
def create_quiz(request):
    if request.method == 'POST':
        form = QuizForm(request.POST, request.FILES)
        if form.is_valid():
            # print(form.cleaned_data)
            uploaded_file = form.cleaned_data['quiz_file']
            x = uploaded_file.read().decode('utf-8')
            quiz_no = form.cleaned_data['quiz_number']
            quiz_name = form.cleaned_data['name']
            quiz_course = form.cleaned_data['course']
            quiz_batch = form.cleaned_data['batch']
            quiz_duration = form.cleaned_data['duration']
            quiz_detail = Quiz(quiz_number=quiz_no,name=quiz_name,course=quiz_course,batch=quiz_batch,duration=quiz_duration)
            quiz_detail.save()
            # print(100)
            j = 0
            # print(x)
            while j < len(x):
                # print(j)
                z = x[j]
                if z == 'Q':
                    question = ""
                    while z != ':':
                        question += z
                        j += 1
                        z = x[j]    

                    j += 1
                    description = ""
                    while z != '?':
                        description += z
                        j += 1
                        z = x[j]
                    description += '?'
                    j += 2
                    z = ''
                    op1, op2, op3, op4 = "", "", "", ""
                    while z!= '.':
                        op1 += z
                        j += 1
                        z = x[j]
                    j += 2
                    z = ''
                    while z != '.':
                        op2 += z
                        j += 1
                        z = x[j]
                    j += 2
                    z = ''
                    while z != '.':
                        op3 += z
                        j += 1
                        z = x[j]
                    j += 2
                    z = ''

                    while z != '.':
                        op4 +=z
                        z = x[j]
                        j += 1

                    print(quiz_no,question, description, op1, op2, op3, op4)
                    q1 = QuizQuestion(quiz_number=quiz_no,question_number=question,
                    question_description=description,
                    option_1=op1,
                    option_2=op2,
                    option_3=op3,
                    option_4=op4)
                    q1.save()
                j += 1
            # print(file_content)
            return redirect('quiz_list')  # Redirect to a page displaying the list of quizzes
    else:
        form = QuizForm()
    return render(request, 'teacher/create_quiz.html', {'form': form})
