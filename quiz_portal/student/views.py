from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
# Create your views here.
def profiles(request):
    return render(request, 'student/profile.html')

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

def home(request):
    return render(request,'student/home.html')