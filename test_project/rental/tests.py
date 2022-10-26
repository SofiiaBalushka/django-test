from datetime import datetime, timedelta
from select import KQ_NOTE_PDATAMASK

from django.test import TestCase
from django.urls import reverse

from rental import models

class RentalTest(TestCase):
    def create_rental(self, name: str ='rental-test'):
        return models.Rental.objects.create(name=name)

    def test_rental_creation(self):
        r = self.create_rental()
        self.assertTrue(isinstance(r, models.Rental))
        self.assertEqual(r.__str__(), r.name)


class ReservationTest(TestCase):
    def create_reservation(self, rental: models.Rental, checkin: datetime =datetime.now(), checkout: datetime =datetime.now()):
        return models.Reservation.objects.create(checkin=checkin, checkout=checkout, rental=rental)

    def test_reservation_creation(self):
        rental = RentalTest().create_rental()
        reservation = self.create_reservation(rental)
        self.assertTrue(isinstance(reservation, models.Reservation))

    def test_reservation_list(self):
        rental = RentalTest().create_rental()
        reservation1 = self.create_reservation(
            rental, 
            checkin=datetime.now() - timedelta(days=14), 
            checkout=datetime.now() - timedelta(days=8)
        )
        reservation2 = self.create_reservation(
            rental, 
            checkin=datetime.now() - timedelta(days=7), 
            checkout=datetime.now()
        )

        reservations_list = models.Reservation.reservations_qs()
        self.assertEqual(reservations_list.count(), 2)

        for reservation in reservations_list:
            if reservation.pk == reservation1.pk:
                self.assertEqual(reservation.prev_reserv_id, None)
            elif reservation.pk == reservation2.pk:
                self.assertEqual(reservation.prev_reserv_id, reservation1.pk)


class ViewsTest(TestCase):
    def setUp(self):
        self.reservations_list_url = reverse('rental:reservations_list')

    def test_reservations_list_view(self):
        rental = RentalTest().create_rental()
        reservation = ReservationTest().create_reservation(rental)

        response = self.client.get(self.reservations_list_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reservations.html')
