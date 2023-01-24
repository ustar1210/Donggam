from datetime import datetime, timedelta
from django.urls import reverse
import calendar
from calender.models import Reservation, RegularReservation
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

class AdminCalendar(calendar.HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(AdminCalendar, self).__init__()

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
        reservations_per_day = reservations.filter(date__day=day)
        d = ''
        try:
            instance = reservations_per_day.get(status='5')
            if instance.name != '' :
                d += f'<li>{instance.name}</li>'
            else :
                d += f'<li>휴일 </li>'
        except:    
            datetime = str(self.year)+'-'+str(self.month)+'-'+str(day)
            h=0
            try:
                am_reserv = reservations_per_day.get(time='10')
                d += f'<li>{am_reserv.get_admin_url} </li>'
                h=1
            except:
                amdatetime = datetime + '-am'
                d += f'<li><label><input type="checkbox"  name="{amdatetime}" style="margin-right:10px">[10:00]</label></li>'
            try:
                pm_reserv = reservations_per_day.get(time='14')
                d += f'<li>{pm_reserv.get_admin_url} </li>'
                h=1
            except:
                pmdatetime = datetime + '-pm'
                d += f'<li><label><input type="checkbox"  name="{pmdatetime}" style="margin-right:10px">[14:00]</label></li>'
            if h==0:
                d += f'<li><label><input type="checkbox"  name="{datetime}" style="margin-right:10px">[휴일]</label></li>'
        if day != 0:
            now_day_class =''
            if day == 25 and now_mont_flag==True:
                if day<10:
                    now_day_class="now_day_point_1"
                else:
                    now_day_class="now_day_point_2"
            return f"<td class='day'><span class='date {now_day_class} day_inner'>{day}</span><ul class='label_inner' style='margin-left:10px;'> {d} </ul></td>"
        
        return '<td></td>'

    def formatweekday(self, day):
        font_color = ''
        if day_abbr[day] == 'Sat':
            font_color = '#0085FF'
        elif day_abbr[day] == 'Sun':
            font_color = '#E92C2C'
        else :
            font_color = '#666666'
        return f'<th class="{self.cssclasses_weekday_head[day]}" style="font-size:16px; color:{font_color}">{day_abbr[day].upper()}</th>'

    def formatweek(self, theweek, reservations):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, reservations)
        return f'<tr class="days"> {week} </tr>'

    def formatmonth(self, withyear=True):
        reservations = Reservation.objects.filter(date__year=self.year, date__month=self.month)
        cal = f'<table border="0" cellpadding="0" cellspacint="0", class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, reservations)}\n'
        cal += f'</table>'
        return cal
