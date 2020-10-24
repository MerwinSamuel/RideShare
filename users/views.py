from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

# Create your views here.
def register(request):
    if request.method=='POST':
        firstName=request.POST['firstName']
        lastName=request.POST['lastName']
        email=request.POST['email']
        username=request.POST['userName']
        password=request.POST['password']
        confirmPassword=request.POST['confirmPassword']
        if password != confirmPassword:
            messages.warning(request,"Passwords do not match. Try again")
            return redirect('/users/register')
        else:
            if User.objects.filter(username=username).exists():
                messages.warning(request,"Username is taken. Try another Username")
                return redirect('/users/register')
            elif User.objects.filter(email=email).exists():
                
                messages.warning(request,"Email is taken. Try another Email")
                return redirect('/users/register')
            else:
                user=User.objects.create_user(username=username,password=password,email=email,first_name=firstName,last_name=lastName)
                user.save()
                messages.success(request,"Registration Successful!")
                return redirect("/users/login")   


    else:
        return render(request,'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request,"Logged In Successfuly!")   
            return redirect("/")
        else:
            messages.warning(request,"Invalid Credentials")
            return redirect('/users/login')
    return render(request, "login.html")

def logout_view(request):
    logout(request)
    messages.info(request,"Logged Out")
    return redirect("/")   