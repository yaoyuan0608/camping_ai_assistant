from django.contrib import admin

# Register your models here.
from .models import Campsite, Reservation, TimeSlot

admin.site.register(Campsite)
admin.site.register(Reservation)
admin.site.register(TimeSlot)