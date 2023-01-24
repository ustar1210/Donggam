from django.shortcuts import render, redirect, get_object_or_404
from calender.models import Reservation, RegularReservation
from manager.utils import AdminCalendar, Weektable
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


        weektable = Weektable(d.year, d.month)
        html_week = weektable.formatmonth(withyear=True)
        context['weektable'] = mark_safe(html_week)

        return context


def admin_save(request):
    if request.user.is_authenticated:
        

        
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
                try :
                    place = get_object_or_404(Place, name='정각원 앞 백년비')
                except : 
                    place = Place()
                    place.name = '정각원 앞 백년비'
                    place.save()
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

def admin_regular_list(request):
    if request.user.is_authenticated:
        instances = RegularReservation.objects.all().order_by('-pk')
        page = request.GET.get('page', '1')
        paginator = Paginator(instances, '10')
        page_obj = paginator.page(page)

        tourdates = RegularDate.objects.filter(date__range=[datetime.datetime.today(), datetime.datetime.today() + datetime.timedelta(days=31)])
        now_sentence = ''
        if len(tourdates.filter(date__month=datetime.datetime.today().month)) > 0:
            now_month_dates = tourdates.filter(date__month=datetime.datetime.today().month)
            now_sentence = str(datetime.datetime.today().month) + '월 정기 캠퍼스투어일은 '
            days = ''
            for d in now_month_dates:
                days += str(d.date.day) + ', '
            now_sentence = now_sentence + days[:-2] + "일 입니다."

        days = ''
        next_sentence = ''
        if len(tourdates.filter(date__month=datetime.datetime.today().month + 1)) > 0 :
            next_month_dates = tourdates.filter(date__month=datetime.datetime.today().month + 1)
            for d in next_month_dates:
                next_sentence = str(d.date.month) + '월 정기 캠퍼스투어일은 '
                days += str(d.date.day) + ', '
            next_sentence = next_sentence + days[:-2] + "일 입니다."

        return render(request, 'manager/regular_list_admin.html', 
        {
            'page_obj': page_obj,
            'now_sentence': now_sentence, 
            'next_sentence': next_sentence,

        })
    else:
        return redirect('manager:login')

def admin_regular_form(request, reservation_id):
    instance = get_object_or_404(RegularReservation, pk = reservation_id)
    if instance.age == 'u':
        age = '14세이상'
    else :
        age = '14세미만'
    if instance.grade == 'n':
        grade = '기타'
    else :
        grade = str(instance.grade) + '학년'
    places = Place.objects.all()
    return render(request, 'manager/regular_form.html', 
    {
        'reservation' : instance,
        'age' : age,
        'grade' : grade,
        'places' : places
    })

def regular_status_change(request, reservation_id):
    if request.user.is_authenticated:
        instance = get_object_or_404(RegularReservation, pk=reservation_id)
        if request.method == "GET":
            instance.status = '3'
        elif request.method == "POST":
            place_name = request.POST['place']
            if place_name == '':
                try :
                    place = get_object_or_404(Place, name='팔정도 코끼리상 앞')
                except : 
                    place = Place()
                    place.name = '팔정도 코끼리상 앞'
                    place.save()
            else :
                try :
                    place = get_object_or_404(Place, name=place_name)
                except :
                    place = Place()
                    place.name = place_name
                    place.save()
            instance.place = place
            instance.admin_comment = request.POST['comment']
            

            instance.status = '2'
        instance.save()
        return redirect('manager:admin_regular_form', reservation_id=reservation_id)
    else:
        return redirect('manager:login')