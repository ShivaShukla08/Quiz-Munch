from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from .models import StudentsProfile, CoreStreams, response_table, Feedback
from . import views                                                   
import math
from django.http import JsonResponse
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from teacher.models import TeacherCourse, TeacherProfile, Quiz_details,Quiz_Question_detail

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

def userlogout(request):
    logout(request)
    messages.info(request,'User was logged out')
    return render(request,'student/login.html')


@login_required
def home(request):
    user_id = request.user.username

    user_details = StudentsProfile.objects.filter(user_id=user_id).first()
    sem = user_details.semester
    stream = user_details.stream
    batch = user_details.batch
 
    course_details = CoreStreams.objects.filter(semester=sem, stream=stream).values()
    
    size =  course_details.count()
    actualheightfcourses = 720
    if(size > 3):   
     actualheightfcourses += (510 * (math.ceil(size/3)-1))

    for course in course_details:
        teacher_details = TeacherCourse.objects.filter(course_id=course['course_id'], batch= batch).first()
        
        if teacher_details:
            teacher_name = TeacherProfile.objects.filter(id = teacher_details.teacher_id).first()
            course['teachername'] = teacher_name.name
        else:
            course['teachername'] = 'Teacher not assigned'
      
        if teacher_details:
            course_id=course['course_id']
            Quiz = Quiz_details.objects.filter(teacher_id = teacher_details.teacher_id, course_id = course_id, batch= batch).values()
            course['total_quiz'] = Quiz.count()
                
    return render(request, 'student/home.html', {"course_details": course_details, "actualheightfcourses": actualheightfcourses})


@login_required
def profile(request):
    user_id = request.user.username
    profile_details = StudentsProfile.objects.filter(user_id=user_id).values()
    return render(request, 'student/profile.html', {"profile_details": profile_details})


@login_required
def quizdisplay(request, quiz_uuid):

    currentTime = datetime.datetime.now().time()
    currentDate = datetime.date.today()

    quizdeatils = Quiz_details.objects.filter(uuid=quiz_uuid).first()
    starttime = quizdeatils.start_time
    endtime = quizdeatils.end_time
    startdate = quizdeatils.start_date
    enddate = quizdeatils.end_date
    user_id = request.user.username
    
    quizResponseDeatils = response_table.objects.filter(uuid=quiz_uuid, sap_id=user_id).values()

    if(startdate < currentDate < enddate):
        if quizResponseDeatils.count() <= 0:
            question = Quiz_Question_detail.objects.filter(uuid=quiz_uuid)
            return render(request, 'student/Quiz_display.html', {'question': question,'quuid':quiz_uuid})
        else:
            return HttpResponse("you are already attempted this quiz.")

    if starttime <= currentTime <= endtime and startdate <= currentDate <= enddate:
        if quizResponseDeatils.count() <= 0:
            question = Quiz_Question_detail.objects.filter(uuid=quiz_uuid)
            return render(request, 'student/Quiz_display.html', {'question': question,'quuid':quiz_uuid})
        else:
            return HttpResponse("you are already attempted this quiz.")
    else:
        if quizResponseDeatils.count() > 0:
            return HttpResponse("you are already attempted this quiz.")
        elif currentDate >= enddate:
            if(currentDate == enddate and endtime < currentTime):
                return HttpResponse("you are missed this quiz today.")
            elif(currentDate > enddate):
                return HttpResponse("you are missed this quiz.")
        
        return HttpResponse("Quizzes are not be started.")
    

@login_required
def studentCourseDetail(request, course_id):
    user_id = request.user.username    
    user_details = StudentsProfile.objects.filter(user_id=user_id).first()
    batch = user_details.batch

    teacher_details = TeacherCourse.objects.filter(course_id = course_id, batch= batch).first()
    details = Quiz_details.objects.filter(teacher_id = teacher_details.teacher_id, course_id = course_id, batch= batch).values()

    # print(details)
    # set myquizes hight in run time
    size =  details.count()
    actualheightfcourses = 590
    if(size > 3):   
     actualheightfcourses += (510 * (math.ceil(size/3)-1))

    return render(request, 'student/Quiz_detail.html', {'details': details, "actualheightfcourses": actualheightfcourses})

 
@login_required
def submit_quiz(request,quiz_uuid):
    user_id = request.user.username    
    if request.method == 'POST':
        total_correct = 0
        total_incorrect = 0

        questions = Quiz_Question_detail.objects.filter(uuid=quiz_uuid)
        print(questions)

        for question in questions:
            selected_option = request.POST.get('q' + str(question.question_number))
            print(question.question_number)
            print(selected_option)
            print(" ")
            ans = selected_option[7]
            
            if ans == question.correct_answer:
                total_correct += 1
            else:
                total_incorrect +=1
        
        result = response_table(uuid=quiz_uuid,sap_id=user_id,total_correct=total_correct, total_incorrect=total_incorrect)
        result.save()

        return JsonResponse({'success': True, 'total_correct': total_correct})
    else:
        print(total_correct)
        return JsonResponse({'error': 'This view only accepts POST requests'}, status=405)

    
@login_required
def notifications(request):
    user_id = request.user.username
    user_details = StudentsProfile.objects.filter(user_id=user_id).first()
    sem = user_details.semester
    stream = user_details.stream
    batch = user_details.batch
 
    course_details = CoreStreams.objects.filter(semester=sem, stream=stream).values()
    details_list = []

    for course in course_details:
        teacher_details = TeacherCourse.objects.filter(course_id=course['course_id'], batch=batch).first()

        if teacher_details:
            course_id = course['course_id']
            course_name = course['course_name']
            teacher_name = teacher_details.teacher.name
            print(teacher_name)
            quizzes = Quiz_details.objects.filter(teacher_id=teacher_details.teacher_id, course_id=course_id, batch=batch).values()
            
            for quiz in quizzes:
                quiz['course_name'] = course_name
                quiz['teacher_name'] = teacher_name
                details_list.append(quiz)

    size = len(details_list)
    actualheightfnotification = 0
    if size > 1:
        actualheightfnotification = (529 * size)

    return render(request, 'student/notifications.html', {'details_list': details_list, 'actualheightfnotification': actualheightfnotification})

@login_required
def feedback(request):
    return render(request, 'student/feedback.html')

from django.http import JsonResponse

@login_required
def submit_feedback(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        rating = request.POST.get('rating')
        feedback = request.POST.get('feedback')
        screenshot = request.FILES.get('quiz-file')

        # Create a new Feedback object and save it to the database
        feedback_obj = Feedback.objects.create(
            name=name,
            email=email,
            rating=rating,
            feedback=feedback,
            screenshot=screenshot
        )

        # Return a JSON response indicating success
        return JsonResponse({'success': True})
    else:
        # Handle other HTTP methods (e.g., GET) if needed
        return JsonResponse({'error': 'Invalid request method'}, status=405)
