# forms.py
from django import forms
from .models import Campsite, Reservation, UserMessage, get_date_choices, TimeSlot
from django.utils import timezone
from datetime import timedelta, datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import EmailValidator

# create a form for reserving campsites
class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['time_slot', 'campsite', 'num_of_people']
        widgets = {
            'campsite': forms.Select(),
            'num_of_people': forms.NumberInput(attrs={'min': 1, 'max': 10}),
        }

    def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)

        # Generate time slots
        date_choices = get_date_choices()
        now = timezone.now().date()
        two_weeks_later = now + timedelta(weeks=2)
        time_slot_choices = []

        for start_date in [now + timedelta(days=i) for i in range(7, (two_weeks_later - now).days + 8)]:
            for end_date in [start_date + timedelta(days=i) for i in range(8, (two_weeks_later - start_date).days + 9)]:
                time_slot, _ = TimeSlot.objects.get_or_create(
                    start_time=start_date, end_time=end_date)
                time_slot_choices.append((time_slot.id, str(time_slot)))

        self.fields['time_slot'] = forms.ChoiceField(choices=time_slot_choices)

# create a form for receiving messages from users
class MessageForm(forms.Form):
    class Meta:
        model = UserMessage
        fields = ['message',]

# create a form for creating  new users
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
