from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from datetime import timedelta, datetime
# Create your models here.
class Campsite(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
def get_date_choices():
    now = timezone.now().date()
    two_weeks_later = now + timedelta(weeks=2)
    choices = [(d.strftime('%Y-%m-%d'), d.strftime('%Y-%m-%d')) for d in [now + timedelta(days=i) for i in range(0, (two_weeks_later - now).days + 1)]]
    return choices

class TimeSlot(models.Model):
    start_time = models.DateField(choices=get_date_choices())
    end_time = models.DateField(choices=get_date_choices())

    def __str__(self):
        return f'{self.start_time} - {self.end_time}'

    def __str__(self):
        return f'{self.start_time} - {self.end_time}'
class Reservation(models.Model):
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    campsite = models.ForeignKey(Campsite, on_delete=models.CASCADE)
    num_of_people = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    is_reserved = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.time_slot} - {self.campsite} - {self.num_of_people}'

    class Meta:
        unique_together = ('time_slot', 'campsite')
        
class UserMessage(models.Model):
    message = models.TextField()
    response = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
