import os
import django
import random
from datetime import datetime, timedelta

# 🔧 Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from airline.models import Flight

cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Hyderabad", "Kolkata"]
airlines = ["IndiGo", "Air India", "SpiceJet", "Vistara"]

for i in range(50):
    source = random.choice(cities)
    destination = random.choice([c for c in cities if c != source])

    date = datetime.now().date() + timedelta(days=random.randint(0, 60))

    departure_time = datetime.now() + timedelta(
        days=random.randint(0, 60),
        hours=random.randint(0, 23)
    )

    arrival_time = departure_time + timedelta(hours=random.randint(1, 5))

    total_seats = random.choice([120, 180, 210])

    Flight.objects.create(
        airline_name=random.choice(airlines),
        source=source,
        destination=destination,
        departure_time=departure_time,
        arrival_time=arrival_time,
        date=date,
        total_seats=total_seats,
        available_seats=total_seats,
        price=random.randint(3000, 12000)
    )

print("✅ Flights added successfully!")