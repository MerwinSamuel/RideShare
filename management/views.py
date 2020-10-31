import json
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from .models import Vehicle,Booking
from .forms import AddForm 
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.db.models import *


import datetime
from django.conf import settings
from django.utils.timezone import make_aware



# Create your views here.
def index(request):
    return render(request,'index.html')

def cars(request):
    vehicle_list = Vehicle.objects.filter(availability=1)
    if not vehicle_list:
        empty = { 'message' : "No Vehicles Available", }
        return render(request, 'cars.html', empty)
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
        post.count = request.POST.get('count')
        post.total_count = post.count
        vhc = Vehicle.objects.filter(make = post.make,model = post.model)
        if vhc.exists()==True:

            vhc_a = Vehicle.objects.get(make = post.make,model = post.model)
            vhc_a.availability = 1
            vhc_a.count += (int)(post.count)
            vhc_a.total_count += (int)(post.count)
            vhc_a.save()
            
        else:
            post.save()
        
        return redirect("/cars")
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
        current_vehicle.count-=1
        current_vehicle.is_booked = True
        if current_vehicle.count <= 0:
            current_vehicle.availability = 0    
        current_vehicle.save()
        return redirect('/cars')

    else:
        if request.user.is_authenticated:
            vehicle = Vehicle.objects.get(pk=vehicleID)
            return render(request, 'booking.html', {'vehicle': vehicle})
        else:
            messages.warning(request,"Please login first!")
            return redirect('/users/login')

def booked(request):
    vehicle_list = Vehicle.objects.filter(is_booked = 1)
    if request.method == 'POST':
        vehicleID = request.POST.get("vehicleID")
        vehicle = Vehicle.objects.get(pk=vehicleID)
        if((vehicle.total_count - vehicle.count) ==1):
            vehicle.is_booked = 0
        else:
            vehicle.is_booked = 1 
        vehicle.count += 1       
        vehicle.save()
        messages.success(request,"Car has been returned successfully!")
        return redirect('/booked')
    if not vehicle_list:
        empty = { 'message' : "All Booked Vehicles Returned", }
        return render(request, 'booked.html', empty)
    else:
        context = {
            'vehicle_list': vehicle_list,
        }
        return render(request, 'booked.html', context)


def dashboard(request):
    current_user = request.user
    booking_list = Booking.objects.filter(userID = current_user.id)
    if not booking_list:
        empty = { 'message' : "No Booking History",}
        return render(request, 'dashboard.html', empty)
    else:
        context = {
            'booking_list': booking_list,
        }
        return render(request, 'dashboard.html', context)


def graph_view(request):
    dataset = Booking.objects \
        .values('VehicleID') \
        .annotate(hours_count=F('hours'),amount_count=F('total')) \
        .order_by('VehicleID')

    categories = list()
    hours_series = list()
    amount_series = list()

    for entry in dataset:
        categories.append('Vehicle No. %s' % entry['VehicleID'])
        hours_series.append(entry['hours_count'])
        amount_series.append(entry['amount_count'])

    return render(request, 'graph.html', {
        'categories': json.dumps(categories),
        'hours_series': json.dumps(hours_series),
        'amount_series': json.dumps(amount_series)
    })
        
