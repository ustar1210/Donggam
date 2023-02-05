from datetime import datetime, timedelta
from django.urls import reverse
import calendar

now = datetime.now().day
now_month = datetime.now().month
import sys
import datetime
import locale as _locale
from itertools import repeat





class _localized_day:

    # January 1, 2001, was a Monday.
    _days = [datetime.date(2001, 1, i+1).strftime for i in range(7)]

    def __init__(self, format):
        self.format = format

    def __getitem__(self, i):
        funcs = self._days[i]
        if isinstance(i, slice):
            return [f(self.format) for f in funcs]
        else:
            return funcs(self.format)

    def __len__(self):
        return 7

class _localized_month:

    _months = [datetime.date(2001, i+1, 1).strftime for i in range(12)]
    _months.insert(0, lambda x: "")

    def __init__(self, format):
        self.format = format

    def __getitem__(self, i):
        funcs = self._months[i]
        if isinstance(i, slice):
            return [f(self.format) for f in funcs]
        else:
            return funcs(self.format)

    def __len__(self):
        return 13

month_name = _localized_month('%B')
day_abbr = _localized_day('%a')
now_mont_flag = False

am_nbsp_flag = False
pm_nbsp_flag = False

class Calendar(calendar.HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()
        

    def formatmonthname(self, theyear, themonth, withyear=True):
        global now_mont_flag
        if withyear:
            if month_name[themonth] == 'January':
                if now_month == 1 :
                    now_mont_flag = True
                else:
                    now_mont_flag =False
                korea_month_name ='1월'
            elif month_name[themonth] == 'February':
                if now_month == 2 :
                    now_mont_flag = True
                else:
                    now_mont_flag =False
                korea_month_name ='2월'
            elif month_name[themonth] == 'March':
                if now_month == 3 :
                    now_mont_flag = True
                else:
                    now_mont_flag =False
                korea_month_name ='3월'
            elif month_name[themonth] == 'April':
                if now_month == 4 :
                    now_mont_flag = True
                else:
                    now_mont_flag =False
                korea_month_name ='4월'
            elif month_name[themonth] == 'May':
                if now_month == 5 :
                    now_mont_flag = True
                else:
                    now_mont_flag =False
                korea_month_name ='5월'
            elif month_name[themonth] == 'June':
                if now_month == 6 :
                    now_mont_flag = True
                else:
                    now_mont_flag =False
                korea_month_name ='6월'
            elif month_name[themonth] == 'July':
                if now_month == 7 :
                    now_mont_flag = True
                else:
                    now_mont_flag =False
                korea_month_name ='7월'
            elif month_name[themonth] == 'August':
                if now_month == 8 :
                    now_mont_flag = True
                else:
                    now_mont_flag =False
                korea_month_name ='8월'
            elif month_name[themonth] == 'September':
                if now_month == 9 :
                    now_mont_flag = True
                else:
                    now_mont_flag =False
                korea_month_name ='9월'
            elif month_name[themonth] == 'October':
                if now_month == 10 :
                    now_mont_flag = True
                else:
                    now_mont_flag =False
                korea_month_name ='10월'
            elif month_name[themonth] == 'November':
                if now_month == 11 :
                    now_mont_flag = True
                else:
                    now_mont_flag =False
                korea_month_name ='11월'
            elif month_name[themonth] == 'December':
                if now_month == 12 :
                    now_mont_flag = True
                else:
                    now_mont_flag =False
                korea_month_name ='12월'
            s = '%s %s' % (theyear,korea_month_name)
        else:
            s = '%s' % month_name[themonth]
        prev_month = f'<a id="prev_month_btn" href="">< </a>'
        next_month = f'<a id="next_month_btn" href=""> > </a>'
        
        return f'<div class="month_name_cal">{prev_month}&nbsp;&nbsp;{s}&nbsp;&nbsp;{next_month}</div>'

    def formatday(self, day, reservations):
        am_nbsp_flag = False 
        pm_nbsp_flag = False
        holiday_flag = False
        reservations_per_day = reservations.filter(date__day=day)
        d = ''
        try:
            instance = reservations_per_day.get(status='5')
            if instance.name != '' :
                d += f'<li class="holiday">{instance.name}</li>'
                holiday_flag = True
            # else :

        except:    
            try:
                am_reserv = reservations_per_day.get(time='10')
                am_nbsp_flag = True
                d += f'<li style="margin-bottom: 10px">{am_reserv.get_html_url} </li>'
            except:
                pass
            try:
                pm_reserv = reservations_per_day.get(time='14')
                pm_nbsp_flag = True
                d += f'<li>{pm_reserv.get_html_url} </li>'
            except:
                pass
        # am은 있지만 pm은 없는 경우  한 줄 추가하기 
        if am_nbsp_flag == True and pm_nbsp_flag == False:
            d += f'<li style="margin-top:10px;">&nbsp;</li>'
        
        # pm은 있지만 am은 없는 경우 한 줄 추가하기 
        elif pm_nbsp_flag == True and am_nbsp_flag == False:
                d += f'<li style="margin-top:10px;">&nbsp;</li>'
        # am, pm 둘다 없는 경우 두 줄 추가하기
        elif am_nbsp_flag == False and pm_nbsp_flag == False:
                d += f'<li>&nbsp;</li>'
                # 휴일 지정되어 있으면 margin-top 주지말기
                if holiday_flag == True:
                    d += f'<li>&nbsp;</li>'
                else: 
                    d += f'<li style="margin-top:10px;">&nbsp;</li>'
            

        if day != 0:
            now_day_class =''
            if day == now and now_mont_flag==True:
                if day<10:
                    now_day_class="now_day_point_1"
                else:
                    now_day_class="now_day_point_2"

            return f"<td class='day'><span class='date {now_day_class}'>{day}</span><ul class='each_day'> {d} </ul></td>"
        
        return '<td></td>'

    def formatweek(self, theweek, reservations):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, reservations)
        return f'<tr class="days"> {week} </tr>'
    
    def formatweekheader(self):
        s = ''.join(self.formatweekday(i) for i in self.iterweekdays())
        return '<tr colspan="7">%s</tr>' % s

    def formatweekday(self, day):
        font_color = ''
        if day_abbr[day] == 'Sat':
            font_color = '#0085FF'
        elif day_abbr[day] == 'Sun':
            font_color = '#E92C2C'
        else :
            font_color = '#666666'
        return f'<th class="{self.cssclasses_weekday_head[day]}" style="font-size:16px; color:{font_color}">{day_abbr[day].upper()}</th>'

    def formatmonth(self, withyear=True):
        reservations = Reservation.objects.filter(date__year=self.year, date__month=self.month)

        cal = f'<table border="0" cellpadding="0" cellspacint="0", class="calendar"">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, reservations)}\n'
        cal += f'</table>\n'
        return cal
        

from django.forms import ModelForm
from calender.models import Reservation, RegularReservation

class ReservationForm(ModelForm):
    class Meta:
        model = Reservation
        fields = ('name', 'phone', 'email', 'school', 'grade', 'major', 'bus', 'headcount', 'length', 'memo')

class RegularReservationForm(ModelForm):
    class Meta:
        model = RegularReservation
        fields = ('date', 'age', 'parent_name', 'parent_phone', 'name', 'phone', 'email', 'school', 'grade', 'headcount', 'motivation', 'request')