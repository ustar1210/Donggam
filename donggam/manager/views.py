from django.shortcuts import render, redirect, get_object_or_404
from calender.models import Reservation, RegularReservation
from manager.utils import AdminCalendar
from django.views import generic
from calender.views import *
from calender.models import *

# Create your views here.
def manager_index(request):
    if request.user.is_authenticated:
        return render(request, 'manager/index.html')
    else:
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

def admin_save(request):
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

def group_form(request, reservation_id):
    instance = get_object_or_404(Reservation, pk=reservation_id)
    if instance.status == '1':
        status = '신청대기'
    elif instance.status == '2':
        status = '검토중'
    elif instance.status == '3':
        status = '승인완료'
    date = str(instance.date).split('-')
    date = date[0] + '년 ' + date[1] + '월 ' + date[2] + '일'
    if instance.time == '10':
        time = '10:00'
    elif instance.time == '14':
        time = '14:00'
    datetime = date + ' / ' + time

    return render(request, 'manager/groupform_admin.html', 
    {
        'reservation' : instance,
        'status': status,
        'datetime': datetime,
    })