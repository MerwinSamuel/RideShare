from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from .models import Vehicle,Booking
from .forms import AddForm 
from django.contrib.auth.models import User,auth
from django.contrib import messages

import datetime
from django.conf import settings
from django.utils.timezone import make_aware



# Create your views here.
def index(request):
    return render(request,'index.html')

def cars(request):
    vehicle_list = Vehicle.objects.filter(availability=1)
    if not vehicle_list:
        return HttpResponse("Vehicle does not exist")
    else:
        context = {
            'vehicle_list': vehicle_list,
        }
        return render(request, 'cars.html', context)

    

def detail(request, vehicleID):
    
    vehicle = Vehicle.objects.get(pk=vehicleID)
    return render(request, 'detail.html', {'vehicle': vehicle})

def add(request):
    if request.method == 'POST':
        post=Vehicle()
        post.make= request.POST.get('make')
        post.model= request.POST.get('model')
        post.imageurl=request.POST.get('imageurl')
        post.mileage= request.POST.get('mileage')
        post.damage= request.POST.get('damage')
        post.seats= request.POST.get('seats')
        post.cost= request.POST.get('cost')
        post.save()
        return HttpResponse("Vehicle Added!")
    else:
        return render(request, 'add.html')

def book(request, vehicleID):
    if request.method == 'POST':
        current_user = request.user
        current_vehicle = Vehicle.objects.get(pk=vehicleID)
        post = Booking()
        post.start=request.POST.get("datetime")
        post.hours=request.POST.get("hours")
        
        post.total=int(request.POST.get("hours")) * current_vehicle.cost
        print(type(request.POST.get("hours")))
        print(type(current_vehicle.cost))
        print(post.total)
        post.VehicleID_id=vehicleID
        post.userID_id=current_user.id
        post.save()
        
        current_vehicle.availability=0
        current_vehicle.save()
        return HttpResponse("Booking Done!")

    else:
        if request.user.is_authenticated:
            vehicle = Vehicle.objects.get(pk=vehicleID)
            return render(request, 'booking.html', {'vehicle': vehicle})
        else:
            messages.warning(request,"Please login first!")
            return redirect('/users/login')
        