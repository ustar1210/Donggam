from django.shortcuts import render, redirect
from calender.models import Reservation, RegularReservation
from manager.utils import AdminCalendar
from django.views import generic
from calender.views import *

# Create your views here.
def login(request):
    return render(request, 'manager/login.html')

def logout(request):
    return redirect('manager:login')


class AdminCalendarView(generic.ListView):
    model = Reservation
    template_name = 'manager/calendarAdmin.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('month', None))
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d) 
        # Instantiate our calendar class with today's year and date
        cal = AdminCalendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)

        return context

def adminsave(request):
    print(request.POST)
    for a in request.POST:
        if a == 'csrfmiddlewaretoken':
            continue
        date = a.split('-', -1)
        yearmonthdate = date[0]+'-'+date[1]+'-'+date[2]
        if date[3] == 'am' :
            time = '10'
        else :
            time = '14'
        instance = Reservation(date=yearmonthdate, time=time, status='0')
        instance.save()
    change_status()
    return redirect('manager:calendarAdmin')