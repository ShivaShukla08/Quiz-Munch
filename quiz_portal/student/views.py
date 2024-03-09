from django.shortcuts import render

# Create your views here.
def profiles(request):
    return render(request, 'student/profile.html')

def loginstudent(request):
    return render(request, 'student/login.html')