from django import forms
from .models import Vehicle

class AddForm(forms.ModelForm): 
   
    '''make = forms.CharField(max_length=30)
    model = forms.CharField(max_length=30)    
    mileage = forms.DecimalField(max_digits=5, decimal_places=2)
    damage = forms.CharField(max_length=200)
    seats = forms.IntegerField()
    cost = forms.IntegerField()'''
    class Meta:
        model = Vehicle
        fields = ['make', 'model', 'mileage', 'damage', 'seats', 'cost']