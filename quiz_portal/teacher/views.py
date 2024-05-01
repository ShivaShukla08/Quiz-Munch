from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
import json, math
from django.http import HttpResponse
from .models import TeacherProfile,TeacherCourse,Quiz,QuizQuestion,Quiz_details,Quiz_Question_detail
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import QuizForm 
import uuid
import pytz  # If you need to work with time zones
from datetime import datetime
from django.contrib import messages
from student.models import response_table, StudentsProfile
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment

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
    details = TeacherCourse.objects.filter(tid=user_id).values()
    
    teachername = TeacherProfile.objects.filter(id=user_id).values('name').first()
    teacher_name = teachername['name']

    # set total no of quizzes in particular course
    for course in details:
        Quiz = Quiz_details.objects.filter(teacher_id = course['tid'], course_id = course['course_id'], batch= course['batch']).values()
        course['total_quiz'] = Quiz.count()

    # set myCouses hight in run time
    size =  details.count()
    actualheightfcourses = 720
    if(size > 3):   
     actualheightfcourses += (510 * (math.ceil(size/3)-1))
     
    return render(request, 'teacher/home.html', {'details': details, 'actualheightfcourses':actualheightfcourses, 'teacher_name':teacher_name})

from django.contrib import messages

def course_detail(request, course_id):
    tid = request.user.username
    details = Quiz_details.objects.filter(course_id=course_id, teacher_id=tid)
    
    size =  details.count()
    actualheightfcourses = 700
    if(size > 3):   
     actualheightfcourses += (600 * (math.ceil(size/3)-1))
    showmessage = False
    if(size == 0):
        actualheightfcourses = 400
        showmessage = True


    if request.method == 'POST':
        # Check if the quiz has been uploaded
        if 'upload_quiz' in request.POST:
            quiz_id = request.POST.get('quiz_id')
            quiz = Quiz_details.objects.get(uuid=quiz_id)
            if not quiz.upload:
                # Perform the upload action
                quiz.upload = True
                quiz.save()
                messages.success(request, 'Quiz uploaded successfully!')
            else:
                messages.warning(request, 'Quiz has already been uploaded.')


    return render(request, 'teacher/course_detail.html', {'details': details, 'actualheightfcourses':actualheightfcourses, 'showmessage':showmessage})

def upload_quiz(request, course_uuid):
    try:
        quiz = Quiz_details.objects.get(uuid=course_uuid)
        quiz.upload = True
        quiz.save()
        messages.success(request, 'Quiz uploaded successfully.')
    except Quiz_details.DoesNotExist:
        messages.error(request, 'Quiz not found.')
    return redirect('course_detail', course_id=quiz.course_id)


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
        # print(x)
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
                
                j = j + 16
                correctans = x[j]
                # print("Details")
                # print(question, description, op1, op2, op3, op4)
                q1 = Quiz_Question_detail(uuid = quiz_uuid,question_number=qnum, question_type="MCQ",
                correct_answer = correctans,
                question_description=description,
                option1=op1,
                option2=op2,
                option3=op3,
                option4=op4)
                print(q1)
                q1.save()
                qnum +=1
            j += 1
        
    user_id = request.user.username
    details = TeacherCourse.objects.filter(tid=user_id)
    return render(request, 'teacher/create_quiz.html', {'details': details})

def quizquestions(request,quiz_uuid):
    questions = Quiz_Question_detail.objects.filter(uuid=quiz_uuid)
    # print(questions)
    return render(request, 'teacher/quiz_display.html', {'questions': questions})


def teacherprofile(request):
    user_id = request.user.username
    profile_details = TeacherProfile.objects.filter(id=user_id).values()
    return render(request, 'teacher/profile.html', {"profile_details": profile_details})

@login_required
def studentresults(request, quiz_uuid):
    responses = response_table.objects.filter(uuid=quiz_uuid)
    # print(responses)
    student_scores = { }

    for response in responses:
        sap_id = response.sap_id
        student_profile = StudentsProfile.objects.filter(user_id=sap_id).first()
        score = response.total_correct
        incorrect = response.total_incorrect
        if student_profile:
            student_scores[student_profile.name] = {'sap_id': sap_id, 'score': score, 'incorrect':incorrect}    
    print(student_scores)

    quizid = quiz_uuid
    
    return render(request, 'teacher/student_results.html', {'student_scores': student_scores, 'quizid': quizid})


@login_required
def generate_excel(request, quizid):
    # Create a new Workbook
    wb = Workbook()
    ws = wb.active
    
    responses = response_table.objects.filter(uuid=quizid)
    
    student_scores = {}

    for response in responses:
        sap_id = response.sap_id
        student_profile = StudentsProfile.objects.filter(user_id=sap_id).first()
        score = response.total_correct
        incorrect = response.total_incorrect
        if student_profile:
            student_scores[student_profile.name] = {'sap_id': sap_id, 'score': score, 'incorrect':incorrect}    

    print(student_scores)

    # Sample data
    # Add headings to data
    data = [
        ['Student Name', 'SAP ID', 'Score', 'Incorrect Question']
    ]

    ws.append(['Student Name', 'SAP ID', 'Score', 'Incorrect Question'])

    # Write data to worksheet
    for student_name, data in student_scores.items():
        # ws.append(['Student Name', 'SAP ID', 'Score', 'Incorrect Question'])
        ws.append([student_name, data['sap_id'], data['score'], data['incorrect']])

    # Apply formatting
    header_font = Font(bold=True)
    header_alignment = Alignment(horizontal='center')
    for cell in ws[1]:
        cell.font = header_font
        cell.alignment = header_alignment

    # Set response headers
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=my_excel_file.xlsx'

    # Save workbook to response
    wb.save(response)

    return response
