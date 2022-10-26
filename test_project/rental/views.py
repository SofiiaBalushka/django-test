from django.shortcuts import render

from rental import models

def reservations_list(request):
    ctx = {
        'reservations': models.Reservation.reservations_qs()
    }
    return render(request, 'reservations.html', ctx)


