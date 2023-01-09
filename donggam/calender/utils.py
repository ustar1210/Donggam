from datetime import datetime, timedelta
import calendar
from .models import Event

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
            d += f'<li><a>[오전 신청가능] </a></li>'
        try:
            pm_reserv = reservations_per_day.get(time='14')
            d += f'<li>{pm_reserv.get_html_url} </li>'
        except:
            d += f'<li><a>[오후 신청가능] </a></li>'

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
        

from django.forms import ModelForm, DateInput
from calender.models import Event, Reservation

class ReservationForm(ModelForm):
    class Meta:
        model = Reservation
        fields = '__all__'


class EventForm(ModelForm):
    class Meta:
        model = Event
        # datetime-local is a HTML5 input type, format to make date time show on fields
        widgets = {
        'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)