from datetime import datetime, timedelta
from django.urls import reverse
import calendar


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

class Calendar(calendar.HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()
        

    def formatmonthname(self, theyear, themonth, withyear=True):
        """
        Return a month name as a table row.
        """
        if withyear:
            if month_name[themonth] == 'January':
                korea_month_name ='1월'
            elif month_name[themonth] == 'February':
                korea_month_name ='2월'
            elif month_name[themonth] == 'March':
                korea_month_name ='3월'
            elif month_name[themonth] == 'April':
                korea_month_name ='4월'
            elif month_name[themonth] == 'May':
                korea_month_name ='5월'
            elif month_name[themonth] == 'June':
                korea_month_name ='6월'
            elif month_name[themonth] == 'July':
                korea_month_name ='7월'
            elif month_name[themonth] == 'August':
                korea_month_name ='8월'
            elif month_name[themonth] == 'September':
                korea_month_name ='9월'
            elif month_name[themonth] == 'October':
                korea_month_name ='10월'
            elif month_name[themonth] == 'November':
                korea_month_name ='11월'
            elif month_name[themonth] == 'December':
                korea_month_name ='12월'
            s = '%s %s' % (theyear,korea_month_name)
        else:
            s = '%s' % month_name[themonth]
        return '<tr><th colspan="7" class="%s" style="color:#585757; font-size:24px;" >%s</th></tr>' % (
            self.cssclass_month_head, s)

    def formatday(self, day, reservations):
        reservations_per_day = reservations.filter(date__day=day)
        d = ''
        try:
            instance = reservations_per_day.get(status='5')
            if instance.name != '' :
                d += f'<li>{instance.name}</li>'
            else :
                d += f'<li></li>'
        except:    
            try:
                am_reserv = reservations_per_day.get(time='10')
                d += f'<li style="margin-bottom: 10px">{am_reserv.get_html_url} </li>'
            except:
                pass
            try:
                pm_reserv = reservations_per_day.get(time='14')
                d += f'<li>{pm_reserv.get_html_url} </li>'
            except:
                pass
        if day != 0:
            return f"<td class='day'><span class='date'>{day}</span><ul class='each_day'> {d} </ul></td>"
        
        return '<td></td>'

    def formatweek(self, theweek, reservations):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, reservations)
        return f'<tr class="days"> {week} </tr>'
    
    def formatweekday(self, day):
        font_color = ''
        if day_abbr[day] == 'Sat':
            font_color = '#0085FF'
        elif day_abbr[day] == 'Sun':
            font_color = '#E92C2C'
        else :
            font_color = '#666666'
        return f'<th class="{self.cssclasses_weekday_head[day]}" style="font-size:16px; color:{font_color}">{day_abbr[day]}</th>'

    def formatmonth(self, withyear=True):
        reservations = Reservation.objects.filter(date__year=self.year, date__month=self.month)

        cal = f'<table border="0" cellpadding="0" cellspacint="0", class="calendar">\n'
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