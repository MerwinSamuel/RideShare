from django.urls import path

from . import views

app_name = 'management'
urlpatterns = [
    path('', views.index, name='index'),
    path('cars/',views.cars,name='cars'),
    path('<int:vehicleID>', views.detail, name='detail'),
    path('add', views.add, name='add'),
    path('<int:vehicleID>/book', views.book, name='book'),
    path('booked/',views.booked, name='booked'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('graph/',views.graph_view, name='graph_view'),
    path('rental/',views.rental, name='rental'),
    
]
