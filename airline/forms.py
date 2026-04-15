from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Flight

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add Bootstrap styling
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class FlightSearchForm(forms.Form):

    CITY_CHOICES = []

    source = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    destination = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    date = forms.DateField(widget=forms.DateInput(attrs={
        'class': 'form-control',
        'type': 'date'
    }))

    sort_by = forms.ChoiceField(
        choices=[
            ('price', 'Price'),
            ('departure', 'Departure Time')
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        sources = Flight.objects.values_list('source', flat=True).distinct()
        destinations = Flight.objects.values_list('destination', flat=True).distinct()

        cities = sorted(set(list(sources) + list(destinations)))

        choices = [(city, city) for city in cities]

        self.fields['source'].choices = choices
        self.fields['destination'].choices = choices

    def clean(self):
        cleaned_data = super().clean()
        source = cleaned_data.get('source')
        destination = cleaned_data.get('destination')

        if source and destination and source == destination:
            raise forms.ValidationError("Source and destination cannot be the same.")

        return cleaned_data
    
class BookingForm(forms.Form):
    num_seats = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    seat_numbers = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g. A1,A2,A3'
        })
    )