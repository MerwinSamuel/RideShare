from django.db import models

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
    availability = models.BooleanField(default=True)

    def __str__(self):
        return (self.make + ' ' +self.model)