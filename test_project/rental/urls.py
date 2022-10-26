from django.urls import path

from rental import views

app_name = 'rental'

urlpatterns = [
	path('reservations_list', views.reservations_list, name='reservations_list')
]