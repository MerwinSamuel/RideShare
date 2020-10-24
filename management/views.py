from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from .models import Vehicle
from .forms import AddForm 

# Create your views here.
def index(request):
    return render(request,'index.html')

def cars(request):
    vehicle_list = Vehicle.objects.all()
    context = {
        'vehicle_list': vehicle_list,
    }
    return render(request, 'cars.html', context)

def detail(request, vehicleID):
    try:
        vehicle = Vehicle.objects.get(pk=vehicleID)
    except Vehicle.DoesNotExist:
        raise Http404("Vehicle does not exist")
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
    