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
    if request.user.is_authenticated:
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
    else :
        return redirect('manager:login')

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
    time = instance.time + ':00'
    datetime = date + ' / ' + time
    if instance.grade == 'n':
        grade = '기타'
    else :
        grade = instance.grade + '학년'
    if instance.major == 0:
        major = '공통'
    elif instance.major == 1:
        major = '문과'
    elif instance.major == 2:
        major = '이과'
    length = str(instance.length)+'0분'

    places = Place.objects.all()
    return render(request, 'manager/groupform_admin.html', 
    {
        'reservation' : instance,
        'status': status,
        'datetime': datetime,
        'grade': grade,
        'major': major,
        'length': length,
        'places': places,
    })


def group_confirm(request, reservation_id):
    if request.user.is_authenticated:
        instance = get_object_or_404(Reservation, pk=reservation_id)
        
        if request.method == 'GET':
            if instance.status == '1':
                instance.status = '2'
                instance.save()
            
        elif request.method == 'POST':
            place_name = request.POST['place']
            if place_name == '':
                place = get_object_or_404(Place, name='정각원 앞 백년비')
            else :
                try :
                    place = get_object_or_404(Place, name=place_name)
                except :
                    place = Place()
                    place.name = place_name
                    place.save()
            instance.place = place
            instance.admin_comment = request.POST['comment']
            
            instance.status = '3'
            instance.save()
            
        return redirect('manager:group_form', reservation_id = reservation_id)
    else :
        return redirect('manager:login')