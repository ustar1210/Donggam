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