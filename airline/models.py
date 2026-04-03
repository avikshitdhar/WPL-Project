# from django.db import models

# # Create your models here.
from django.db import models
from django.contrib.auth.models import User
import string
from django.db.models.signals import post_save
from django.dispatch import receiver

# ✈️ Flight Model
class Flight(models.Model):
    airline_name = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)

    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    date = models.DateField()

    SEAT_CHOICES = [
        (120, '120 Seats'),
        (180, '180 Seats'),
        (210, '210 Seats'),
    ]

    total_seats = models.IntegerField(choices=SEAT_CHOICES)
    available_seats = models.IntegerField()
    # available_seats = models.IntegerField()

    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.airline_name} | {self.source} → {self.destination} | {self.date}"


# 🎟️ Booking Model
class Booking(models.Model):
    STATUS_CHOICES = [
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)

    num_seats = models.IntegerField()
    seat_numbers = models.CharField(max_length=100)  # e.g. "A1,A2,A3"

    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='CONFIRMED')
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.id} | {self.user.username} | {self.flight}"


# 👤 Profile Model (optional but useful)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.user.username
    
class Seat(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=5)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.flight.id} - {self.seat_number}"
    
def generate_seats(flight):
    rows = list(string.ascii_uppercase)  # A, B, C...
    seats_per_row = 6  # A1–A6 typical

    total = flight.total_seats
    count = 0

    for row in rows:
        for num in range(1, seats_per_row + 1):
            if count >= total:
                return
            seat_number = f"{row}{num}"
            Seat.objects.create(flight=flight, seat_number=seat_number)
            count += 1

@receiver(post_save, sender=Flight)
def create_seats(sender, instance, created, **kwargs):
    if created:
        instance.available_seats = instance.total_seats
        instance.save()
        generate_seats(instance)