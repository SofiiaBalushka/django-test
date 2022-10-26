from datetime import datetime, timedelta

from django.db import models
from django.db.models import OuterRef, Subquery

class Rental(models.Model):
    name = models.TextField()

    class Meta:
        db_table = 'rentals'

    def __str__(self):
        return f'{self.name}'


class Reservation(models.Model):
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE)
    checkin = models.DateTimeField()
    checkout = models.DateTimeField()

    class Meta:
        db_table = 'reservations'
    

    @classmethod 
    def reservations_qs(cls):
        return cls.objects\
        .annotate(
            prev_reserv_id=Subquery(
                cls.objects.filter(
                    rental=OuterRef('rental'),
                    checkout__lte=OuterRef('checkin')
                ).order_by('-checkout').values('pk')[:1]
            )
        )\
        .all()
