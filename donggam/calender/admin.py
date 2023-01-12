from django.contrib import admin
from calender.models import Place, Reservation, RegularReservation, RegularDate

admin.site.register(Reservation)
admin.site.register(Place)
admin.site.register(RegularReservation)
admin.site.register(RegularDate)