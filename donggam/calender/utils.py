from datetime import datetime, timedelta
from django.urls import reverse
import calendar

class Calendar(calendar.HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    def formatday(self, day, reservations):
        reservations_per_day = reservations.filter(date__day=day)
        d = ''
        try:
            am_reserv = reservations_per_day.get(time='10')
            d += f'<li>{am_reserv.get_html_url} </li>'
        except:
            pass
        try:
            pm_reserv = reservations_per_day.get(time='14')
            d += f'<li>{pm_reserv.get_html_url} </li>'
        except:
            pass
        if day != 0:
            return f"<td class='day'><span class='date'>{day}</span><ul> {d} </ul></td>"
        
        return '<td></td>'

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
        return cal
        

class AdminCalendar(calendar.HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(AdminCalendar, self).__init__()

    def formatday(self, day, reservations):
        reservations_per_day = reservations.filter(date__day=day)
        d = ''
        datetime = str(self.year)+'-'+str(self.month)+'-'+str(day)
        try:
            am_reserv = reservations_per_day.get(time='10')
            d += f'<li>{am_reserv.get_html_url} </li>'
        except:
            amdatetime = datetime + '-am'
            d += f'<li><label><input type="checkbox" name="{amdatetime}">[10:00]</label></li>'
        try:
            pm_reserv = reservations_per_day.get(time='14')
            d += f'<li>{pm_reserv.get_html_url} </li>'
        except:
            pmdatetime = datetime + '-pm'
            d += f'<li><label><input type="checkbox" name="{pmdatetime}">[14:00]</label></li>'
        if day != 0:
            return f"<td class='day'><span class='date'>{day}</span><ul> {d} </ul></td>"
        
        return '<td></td>'

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
        return cal

from django.forms import ModelForm
from calender.models import Reservation

class ReservationForm(ModelForm):
    class Meta:
        model = Reservation
        fields = ('age', 'name', 'email', 'school', 'grade', 'headcount', 'phone', 'motivation', 'request')

