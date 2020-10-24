from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.http import HttpResponseRedirect
from django.urls import reverse

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
            
            return render(request, 'register.html', {
                "message": "Passwords do not match. Try again."
            })

            
        else:
            
            if User.objects.filter(username=username).exists():
                
               return render(request, 'register.html', {
                    "message": "Username is taken. Try another Username."
                })
            elif User.objects.filter(email=email).exists():
                
                return render(request, 'register.html', {
                    "message": "There is already an account with this Email."
                }) 
            else:
                user=User.objects.create_user(username=username,password=password,email=email,first_name=firstName,last_name=lastName)
                user.save()
                print("user created")
                return redirect("login")   


    else:
        return render(request,'register.html')

def index(request):    
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "index.html")

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "login.html", {
                "message": "Invalid Credentials."
            })
    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return render(request, "login.html", {
        "message" : "Logged Out."
    })