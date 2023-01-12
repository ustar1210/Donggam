from django.contrib import admin
from calender.models import Place, Reservation

admin.site.register(Reservation)
admin.site.register(Place)