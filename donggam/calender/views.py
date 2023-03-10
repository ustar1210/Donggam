import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.utils.safestring import mark_safe
from django.urls import reverse
from .models import *
import calendar
from .utils import Calendar, ReservationForm, RegularReservationForm

import smtplib
from email.mime.text import MIMEText


def index(request):
    return render(request, 'calender/index.html')

def group_notice(request):
    return render(request, 'calender/group_notice.html')

def regular_notice(request):
    return render(request, 'calender/regular_notice.html')

class CalendarView(generic.ListView):
    model = Reservation
    template_name = 'calender/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('month', None))
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d) 
        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)

        change_status()
        return context


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return datetime.date(year, month, day=1)
    return datetime.datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - datetime.timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + datetime.timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month



from django.conf import settings
school_email = getattr(settings, 'EMAIL', None)
email_pw = getattr(settings, 'EMAIL_PW', None)
school_phone = getattr(settings, 'PHONE', None)
# ?????? ?????????
# ???????????? 
def requestMail(a, instance):
    # ?????? ??????
    s = smtplib.SMTP('smtp.gmail.com', 587)
    # TLS ?????? ??????
    s.starttls()
    # ????????? ??????
    s.login(school_email, email_pw)
    if a == '??????':
        msg = MIMEText(f"{instance.date} {instance.school}???(???) {a}?????????????????? ??????????????????.")
        msg['Subject'] = f'[??????] {instance.date} {instance.school} {a}??????????????? ??????'
    else :
        days = ['???', '???', '???', '???', '???', '???', '???']
        day = instance.date.weekday()
        msg = MIMEText(f"{instance.date.month}??? {instance.date.day}???({days[day]}) {instance.school}???(???) {a}?????????????????? ??????????????????.")
        msg['Subject'] = f'[??????] {instance.date.month}??? {instance.date.day}???({days[day]}) {instance.school} {a}??????????????? ??????'

    s.sendmail(school_email,school_email, msg.as_string())
    # ?????? ??????
    s.quit()

# ??????????????? ????????????????????? ?????????????????? ?????? ????????? 
def statusMail(a, instance, result):
    # ?????? ??????
    s = smtplib.SMTP('smtp.gmail.com', 587)
    # TLS ?????? ??????
    s.starttls()
    # ????????? ??????
    s.login(school_email, email_pw)
    if a == '??????':
        msg = MIMEText(f"{instance.date} {instance.school}??? ??????????????? {a}????????? ??????????????? {result}???????????????. \n????????? : {school_phone}")
        msg['Subject'] = f'[??????] {instance.date} {instance.school} {a}??????????????? ????????????'
    else :
        days = ['???', '???', '???', '???', '???', '???', '???']
        day = instance.date.weekday()
        msg = MIMEText(f"{instance.date.month}??? {instance.date.day}???({days[day]}) {instance.school}??? ??????????????? {a}????????? ??????????????? {result}???????????????. \n????????? : {school_phone}")
        msg['Subject'] = f'[??????] {instance.date.month}??? {instance.date.day}???({days[day]}) {instance.school} {a}??????????????? ????????????'
    s.sendmail(school_email, instance.email, msg.as_string())
    # ?????? ??????
    s.quit()

def reservation(request, reservation_id=None):
    instance = get_object_or_404(Reservation, pk=reservation_id)
    if instance.email != None:
        email_front = instance.email.split('@')[0]
        email_back = instance.email.split('@')[1]
        state = 1
    else : 
        email_front = ''
        email_back = ''
        state = 0
    if request.method == 'POST':
        if instance.status == '1' or instance.status == '0':    
            if request.POST['agree'] == 'on' and int(request.POST['headcount']) >= 10 and int(request.POST['headcount']) < 101:
                try : 
                    instance.status = '1'
                    instance.name = request.POST['name']
                    phone = request.POST['phone']
                    instance.phone = phone.replace('-', '')
                    instance.email = request.POST['email_front'] + '@' +request.POST['email_back']
                    instance.school = request.POST['school']
                    instance.grade = request.POST['grade']
                    instance.major = int(request.POST['major'])
                    instance.bus = request.POST['bus']
                    instance.headcount = request.POST['headcount']
                    instance.length = int(request.POST['length'])
                    instance.memo = request.POST['memo']
                    instance.save()   
                    requestMail('??????', instance) 
                    return HttpResponseRedirect(reverse('calender:calendar'), {
                        'text' : '?????? ?????????????????????.'
                    })
                except:
                    return redirect('calender:reservation_edit', reservation_id=reservation_id)
            else :
                return redirect('calender:reservation_edit', reservation_id=reservation_id)
        else :
            return redirect('calender:reservation_check', reservation_id=reservation_id)
    return render(request, 'calender/reservation.html', {
        'reservation': instance,
        'state': state,
        'email_front': email_front,
        'email_back': email_back,
        })

def reservationCheck(request, reservation_id):
    instance = get_object_or_404(Reservation, pk=reservation_id)
    if instance.status == '1':
        status = '????????????'
    elif instance.status == '2':
        status = '?????????'
    elif instance.status == '3':
        status = '????????????'
    date = str(instance.date).split('-')
    date = date[0] + '??? ' + date[1] + '??? ' + date[2] + '???'
    time = instance.time + ':00'
    datetime = date + ' / ' + time
    return render(request, 'calender/group_check.html', 
    {
        'reservation' : instance,
        'status': status,
        'datetime': datetime,
    })

def password(request, reservation_id):
    return render(request, 'calender/password.html', {'reservation_id' : reservation_id})

def pw_check(request, reservation_id):
    instance = get_object_or_404(Reservation, pk=reservation_id)
    password = instance.phone[-4:]
    if password == request.POST['pw']:
        return redirect('calender:reservation_edit', reservation_id=reservation_id)
    else :
        return redirect('calender:password', reservation_id = reservation_id)

def change_status():
    print(datetime.datetime.today())
    beforedates = Reservation.objects.filter(date__range=[datetime.datetime.today() - datetime.timedelta(days=30), datetime.datetime.today() - datetime.timedelta(days=1)])
    targets = beforedates.filter(status = '0')
    for t in targets:
        t.status = '4'
        t.save()
    return 

from django.core.paginator import Paginator

def regular_list(request):
    instances = RegularReservation.objects.all().order_by('-pk')
    page = request.GET.get('page', '1')
    paginator = Paginator(instances, '10')
    page_obj = paginator.page(page)

    tourdates = RegularDate.objects.filter(date__range=[datetime.datetime.today(), datetime.datetime.today() + datetime.timedelta(days=91)]).order_by('date')

    return render(request, 'calender/regular_list.html', 
    {
        'page_obj': page_obj,
        'tourdates': tourdates,
    })

def regular_form(request, reservation_id=None):
    if reservation_id != None:
        instance = get_object_or_404(RegularReservation, pk=reservation_id)
        email_front = instance.email.split('@')[0]
        email_back = instance.email.split('@')[1]
        state = 1
        text = '???????????? ????????? ?????????????????????.'
    else :
        instance = RegularReservation()
        email_front = '' 
        email_back = ''
        state = 0
        text = '???????????? ????????? ?????????????????????.'

    tourdates = RegularDate.objects.filter(date__range=[datetime.datetime.today(), datetime.datetime.today() + datetime.timedelta(days=31)])

    if request.POST:
        if request.POST['agree'] == 'on' and int(request.POST['headcount']) >= 10 and int(request.POST['headcount']) < 101 :
            try:
                instance.status = '1'
                instance.age = request.POST['age']
                instance.parent_name = request.POST['parent_name']
                parent_phone = request.POST['parent_phone']
                instance.parent_phone = parent_phone.replace('-', '')
                instance.name = request.POST['name']
                phone = request.POST['phone']
                instance.phone = phone.replace('-', '')
                instance.email = request.POST['email_front'] + '@' +request.POST['email_back']
                instance.school = request.POST['school']
                instance.grade = request.POST['grade']
                instance.headcount = request.POST['headcount']
                instance.date = get_object_or_404(RegularDate, date = request.POST['date'])
                instance.motivation = request.POST['motivation']
                instance.request = request.POST['request']
                instance.save() 
                
                requestMail('??????', instance)    
                return redirect('calender:regular_detail', reservation_id = instance.pk)
            except :
                if state == 1:
                    return redirect('calender:regular_form', reservation_id=reservation_id)    
                else :
                    return redirect('calender:regular_form')
        else :
            if state == 1:
                return redirect('calender:regular_form', reservation_id=reservation_id)    
            else :
                return redirect('calender:regular_form')

    return render(request, 'calender/regular_form.html', {
        'reservation': instance,
        'state': state,
        'dates': tourdates,
        'email_front': email_front,
        'email_back': email_back,
        })

def regular_detail(request, reservation_id):
    instance = get_object_or_404(RegularReservation, pk = reservation_id)
    if instance.age == 'u':
        age = '14?????????'
    else :
        age = '14?????????'
    if instance.grade == 'n':
        grade = '??????'
    else :
        grade = str(instance.grade) + '??????'
    return render(request, 'calender/regular_detail.html', 
    {
        'reservation' : instance,
        'age' : age,
        'grade' : grade,

    })

def regular_pw(request, reservation_id):
    if request.method ==  'GET':
        return render(request, 'calender/regular_password.html', {'reservation_id' : reservation_id})
    
    elif request.method == 'POST':
        instance = get_object_or_404(RegularReservation, pk=reservation_id)
        password = instance.phone[-4:]
        if password == request.POST['pw']:
            return redirect('calender:regular_detail', reservation_id = reservation_id)
        else :
            return redirect('calender:regular_pw', reservation_id = reservation_id)

def regular_delete(request, reservation_id):
    instance = get_object_or_404(RegularReservation, pk = reservation_id)
    instance.delete()
    return redirect('calender:regular_list')