from django.shortcuts import render, get_object_or_404, redirect
from .models import Flight, Booking, Seat
from .forms import FlightSearchForm, BookingForm, SignupForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.utils import timezone


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignupForm()

    return render(request, 'airline/signup.html', {'form': form})


@login_required
def home(request):
    form = FlightSearchForm()
    return render(request, 'airline/home.html', {'form': form})


@login_required
def search_results(request):
    form = FlightSearchForm(request.GET)
    flights = []

    if form.is_valid():
        source = form.cleaned_data['source']
        destination = form.cleaned_data['destination']
        date = form.cleaned_data['date']
        sort_by = form.cleaned_data.get('sort_by')

        flights = Flight.objects.filter(
            source__iexact=source,
            destination__iexact=destination,
            date=date,
            available_seats__gt=0
        )

        if sort_by == 'price':
            flights = flights.order_by('price')
        elif sort_by == 'departure':
            flights = flights.order_by('departure_time')

    return render(request, 'airline/search_results.html', {
        'form': form,
        'flights': flights,
        'now': timezone.now()
    })


@login_required
def book_flight(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)

    if timezone.now() > flight.departure_time:
        return render(request, 'airline/error.html', {
            'message': 'This flight has already departed. Booking is closed.'
        })

    available_seats = Seat.objects.filter(flight=flight)

    if request.method == 'POST':
        selected_seats = request.POST.getlist('seats')

        if not selected_seats:
            return render(request, 'airline/booking.html', {
                'flight': flight,
                'seats': available_seats,
                'error': 'Please select at least one seat.'
            })

        if len(selected_seats) > flight.available_seats:
            return render(request, 'airline/booking.html', {
                'flight': flight,
                'seats': available_seats,
                'error': 'Not enough seats available!'
            })

        total_price = len(selected_seats) * flight.price

        seat_objs = Seat.objects.filter(id__in=selected_seats)
        seat_numbers = ",".join(seat_objs.values_list('seat_number', flat=True))

        booking = Booking.objects.create(
            user=request.user,
            flight=flight,
            num_seats=len(selected_seats),
            seat_numbers=seat_numbers,
            total_price=total_price,
            status='CONFIRMED'
        )

        for seat in seat_objs:
            seat.is_booked = True
            seat.save()

        flight.available_seats -= len(selected_seats)
        flight.save()

        return redirect('payment', booking_id=booking.id)

    return render(request, 'airline/booking.html', {
        'flight': flight,
        'seats': available_seats
    })


@login_required
def payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        return redirect('invoice', booking_id=booking.id)

    return render(request, 'airline/payment.html', {'booking': booking})


@login_required
def invoice(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'airline/invoice.html', {'booking': booking})


@login_required
def profile(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')

    return render(request, 'airline/profile.html', {
        'bookings': bookings
    })