from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('search/', views.search_results, name='search_results'),
    path('book/<int:flight_id>/', views.book_flight, name='book_flight'),
    path('payment/<int:booking_id>/', views.payment, name='payment'),
    path('invoice/<int:booking_id>/', views.invoice, name='invoice'),
    path('profile/', views.profile, name='profile'),
    path('signup/', views.signup, name='signup'),
]