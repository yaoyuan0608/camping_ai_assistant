# forms.py
from django import forms
from .models import Campsite, Reservation, UserMessage


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['time_slot', 'campsite', 'num_of_people']
        widgets = {
            'time_slot': forms.Select(),
            'campsite': forms.Select(),
            'num_of_people': forms.NumberInput(attrs={'min': 1, 'max': 10}),
        }


class MessageForm(forms.Form):
    class Meta:
        model = UserMessage
        fields = ['message',]
