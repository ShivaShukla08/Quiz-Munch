from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
import json
from django.http import HttpResponse
from .models import TeacherProfile,TeacherCourse,Quiz,QuizQuestion,Quiz_details,Quiz_Question_detail
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import QuizForm 
import uuid
import pytz  # If you need to work with time zones
from datetime import datetime

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
    return render(request, 'teacher/home.html', {'details': details})


def course_detail(request,course_id):
    tid = request.user.username
    details = Quiz_details.objects.filter(course_id=course_id, teacher_id=tid)
    print(details)
    return render(request, 'teacher/course_detail.html', {'details': details})

@login_required
def create_quiz(request):
    if request.method == 'POST':
        form = QuizForm(request.POST, request.FILES)
        tid = request.user.username
        quiz_name = request.POST.get('quiz-name')
        quiz_uuid = uuid.uuid4()
        
        start_time_str = request.POST.get('start-time')
        end_time_str = request.POST.get('end-time')
     
        if start_time_str and end_time_str:
            start_time = datetime.strptime(start_time_str, '%H:%M').time()
            end_time = datetime.strptime(end_time_str, '%H:%M').time()
        else:
            start_time = None
            end_time = None
   
        start_date_str = request.POST.get('start-date')
        end_date_str = request.POST.get('end-date')
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        course_and_batch = request.POST.get('course') 
        words = course_and_batch.split("-")
        course_id = words[0]
        course_name = words[1]
        stream = ""
        backtracking = False
        upload = False
        batch = words[2]



        quiz_detail = Quiz_details(
            teacher_id=tid,
            quiz_name=quiz_name,
            uuid=quiz_uuid,
            start_time=start_time,
            end_time=end_time,
            start_date=start_date,
            end_date=end_date,
            course_id=course_id,
            batch=batch,
            stream=stream,
            backtracking=backtracking,
            upload=upload
        )

        print(quiz_name)
        # Save the instance to the database
        quiz_detail.save()
        quiz_file = request.FILES.get('quiz-file')
        x = quiz_file.read()
        x = x.decode('utf-8')

        j = 0
        qnum = 1
        while j < len(x):
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
                j += 1
                z = ''
                op1, op2, op3, op4 = "", "", "", ""
                while z!= '.':
                    op1 += z
                    j += 1
                    z = x[j]
                j += 1
                z = ''
                while z != '.':
                    op2 += z
                    j += 1
                    z = x[j]
                j += 1
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
                print("Details")
                print(question, description, op1, op2, op3, op4)
                q1 = Quiz_Question_detail(uuid = quiz_uuid,question_number=qnum, question_type="MCQ",
                correct_answer = "A",
                question_description=description,
                option1=op1,
                option2=op2,
                option3=op3,
                option4=op4)
                q1.save()
                qnum +=1
            j += 1
        

    user_id = request.user.username
    details = TeacherCourse.objects.filter(tid=user_id)
    return render(request, 'teacher/create_quiz.html', {'details': details})


def quizquestions(request,quiz_uuid):
    questions = Quiz_Question_detail.objects.filter(uuid=quiz_uuid)
    print(questions)
    return render(request, 'teacher/quiz_display.html', {'questions': questions})


def teacherprofile(request):
    user_id = request.user.username
    profile_details = TeacherProfile.objects.filter(id=user_id).values()
    return render(request, 'teacher/profile.html', {"profile_details": profile_details})