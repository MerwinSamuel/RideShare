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
from django.db import connection



import datetime
from django.conf import settings
from django.utils.timezone import make_aware



# Create your views here.
def index(request):
    return render(request,'index.html')

def cars(request):
    vehicle_list = Vehicle.objects.filter(availability=1)
    if request.method == 'POST':
        global seatslower
        global seatsupper
        global mileagelower
        global mileageupper
        global pricelower
        global priceupper
        seatslower = int(float(request.POST.get('seats-lower')))
        seatsupper = int(float(request.POST.get('seats-upper')))
        mileagelower = int(float(request.POST.get('mileage-lower')))
        mileageupper = int(float(request.POST.get('mileage-upper')))
        pricelower = int(float(request.POST.get('price-lower')))
        priceupper = int(float(request.POST.get('price-upper')))

        vehicle_list = Vehicle.objects.filter(availability=1,seats__range=[seatslower,seatsupper],mileage__range=[mileagelower,mileageupper],cost__range=[pricelower,priceupper])
    if request.method == 'GET':
        try:
            seatslower
        except NameError:
            seatslower = 0
            seatsupper = 10
            mileagelower =0
            mileageupper = 30
            pricelower = 0
            priceupper = 30000
        if request.GET.get('sort') == 'high':
            vehicle_list = Vehicle.objects.filter(availability=1,seats__range=[seatslower,seatsupper],mileage__range=[mileagelower,mileageupper],cost__range=[pricelower,priceupper]).order_by('-cost')
        elif request.GET.get('sort') == 'low':
            vehicle_list = Vehicle.objects.filter(availability=1,seats__range=[seatslower,seatsupper],mileage__range=[mileagelower,mileageupper],cost__range=[pricelower,priceupper]).order_by('cost')
        else:
            pass
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
        post.status=1
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
    booking_list = Booking.objects.filter(status=1)
    if request.method == 'POST':
        bookingID = request.POST.get("bookingID")
        booking = Booking.objects.get(pk=bookingID)
        vehicleID = request.POST.get("vehicleID")
        vehicle = Vehicle.objects.get(pk=vehicleID)
        if((vehicle.total_count - vehicle.count) ==1):
            vehicle.is_booked = 0
        else:
            vehicle.is_booked = 1 
        
        vehicle.availability=1
        vehicle.count += 1       
        vehicle.save()

        if vehicle.availability==1:
        	with connection.cursor() as cursor:
        		cursor.execute("UPDATE management_booking SET status = 0 WHERE bookingID = %s", [booking.bookingID])

        
       
        

        messages.success(request,"Car has been returned successfully!")
        return redirect('/booked')
    if not vehicle_list:
        empty = { 'message' : "All Booked Vehicles Returned", }
        return render(request, 'booked.html', empty)
    else:
        context = {
            'vehicle_list': vehicle_list,
            'booking_list': booking_list,
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

def rental(request):
    return render(request, 'rental.html')


def graph_view(request):
    dataset = Booking.objects.raw('SELECT distinct(VehicleID_id) as vid, sum(hours) as hours_count,sum(total) as amount_count,bookingID FROM management_booking GROUP BY VehicleID_id ORDER BY VehicleID_id')
    #dataset1 = Vehicle.objects.raw('SELECT model from management_vehicle where VehicleID in (select VehicleID_id from management_booking)')

   
      #  .values('VehicleID') \
      #  .annotate(hours_count=sum('hours'),amount_count=sum('total')) \
      #  .group_by('VehicleID') \
      #  .order_by('VehicleID')    

    categories = list()
    hours_series = list()
    amount_series = list()

        
    for entry in dataset:
        vehicle = Vehicle.objects.get(pk=entry.vid)
        name = vehicle.make + " " + vehicle.model
        categories.append('%s' % name)
        hours_series.append((int)(entry.hours_count))
        amount_series.append((int)(entry.amount_count))



    return render(request, 'graph.html', {
        'categories': json.dumps(categories),
        'hours_series': json.dumps(hours_series),
        'amount_series': json.dumps(amount_series)
    })
        
