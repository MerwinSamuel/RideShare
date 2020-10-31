from django.db import models
from django.conf import settings

# Create your models here.
class Vehicle(models.Model):
    vehicleID = models.AutoField(primary_key=True)
    make = models.CharField(max_length=30)
    model = models.CharField(max_length=30)
    imageurl = models.CharField(max_length=500)    
    mileage = models.DecimalField(max_digits=5, decimal_places=2)
    damage = models.CharField(max_length=200)
    seats = models.IntegerField()
    cost = models.IntegerField()
    count = models.IntegerField(default = 1)
    total_count = models.IntegerField(default = 1)
    availability = models.BooleanField(default=True)
    is_booked = models.BooleanField(default = False)

   



    


class Booking(models.Model):
    bookingID = models.AutoField(primary_key=True)
    VehicleID = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    userID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start = models.DateTimeField()
    hours = models.IntegerField()
    total = models.IntegerField()
