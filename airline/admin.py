from django.contrib import admin
from .models import Flight, Booking, Profile

admin.site.register(Flight)
admin.site.register(Booking)
admin.site.register(Profile)