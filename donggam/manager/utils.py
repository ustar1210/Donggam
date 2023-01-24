from datetime import datetime, timedelta
from django.urls import reverse
import calendar
from calender.models import Reservation, RegularReservation
from django.db.models import Q

class AdminCalendar(calendar.HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(AdminCalendar, self).__init__()

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
            try:
                am_reserv = reservations_per_day.get(time='10')
                d += f'<li>{am_reserv.get_admin_url} </li>'
            except:
                pass
            try:
                pm_reserv = reservations_per_day.get(time='14')
                d += f'<li>{pm_reserv.get_admin_url} </li>'
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
        cal += f'</table>'
        return cal

class Weektable(calendar.HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Weektable, self).__init__()

    def formatday(self, day, reservations):
        a=''
        b=f'<li>오전</li><li>오후</li>'
        c=''
        d=''
        e=''
        reservations_per_day = reservations.filter(date__day=day)
        status = []
        for r in reservations_per_day:
            status.append(r.status)

        
        if '5' in status:
            a += f'<li><input type="checkbox" id="open" name="open" value="on"></li><li><input type="checkbox" id="open" name="open" value="on"></li>'
            d += f"""<li><select id="status"><option value="주말">주말</option><option value="비개방">비개방</option></select></li>
            <li><select id="status"><option value="주말">주말</option><option value="비개방">비개방</option></select></li>"""
        elif '7' in status:
            a += f'<li><input type="checkbox" id="open" name="open" value="on"></li><li><input type="checkbox" id="open" name="open" value="on"></li>'
            d += f"""<li><select id="status"><option value="주말">주말</option><option value="비개방">비개방</option></select></li>
            <li><select id="status"><option value="주말">주말</option><option value="비개방">비개방</option></select></li>"""
            e += f"""<li><input type="text" name="reason"></li><li><input type="text" name="reason"></li>"""
        else :
            a += f'<li><input type="checkbox" id="open" name="open" value="on" checked></li><li><input type="checkbox" id="open" name="open" value="on" checked></li>'
            try :
                am_reserv = reservations_per_day.get(time='10')
                # 오전 예약의 상태에 따라서 바뀜
                if am_reserv.status == '0':
                    c += f'<li></li>'
                    d += f"""<li>신청대기</li>"""
                    e += f'<li></li>'
                elif am_reserv.status == '1' or am_reserv.status == '2' or am_reserv.status == '3':
                    c += f'<li style="margin-bottom: 10px">{am_reserv.school} </li>'
                    d += f"""<li style="margin-bottom: 10px">
                        <select id="status">
                            <option value="신청가능">신청가능</option>
                            <option value="신청대기">신청대기</option>
                            <option value="검토중">검토중</option>
                            <option value="승인완료">승인완료</option>
                            <option value="거부">거부</option>
                        </select>
                        </li>"""
                    e += '<li></li>'
                elif am_reserv.status == '4':
                    c += f'<li></li>'
                    d += f"""<li>신청마감</li>"""
                    e += f'<li></li>'
                elif am_reserv.status == '6':
                    c += f'<li style="margin-bottom: 10px">{am_reserv.school} </li>'
                    d += f"""<li style="margin-bottom: 10px">
                        <select id="status">
                            <option value="신청가능">신청가능</option>
                            <option value="신청대기">신청대기</option>
                            <option value="검토중">검토중</option>
                            <option value="승인완료">승인완료</option>
                            <option value="거부">거부</option>
                        </select>
                        </li>"""
                    e += f"""<li><input type="text" name="reason"></li><li><input type="text" name="reason"></li>"""
            except :
                if day < datetime.today().day:
                    c += f'<li></li>'
                    d += f"""<li>신청대기</li>"""
                    e += f'<li></li>'
                else :
                    c += f'<li></li>'
                    d += f"""<li>신청마감</li>"""
                    e += f'<li></li>'
            try :
                # 오후 예약의 상태에 따라서 바뀜
                pm_reserv = reservations_per_day.get(time='14')
                if pm_reserv.status == '0':
                    c += f'<li></li>'
                    d += f"""<li>신청대기</li>"""
                    e += f'<li></li>'
                elif pm_reserv.status == '1' or pm_reserv.status == '2' or pm_reserv.status == '3':
                    c += f'<li style="margin-bottom: 10px">{pm_reserv.school} </li>'
                    d += f"""<li style="margin-bottom: 10px">
                        <select id="status">
                            <option value="신청가능">신청가능</option>
                            <option value="신청대기">신청대기</option>
                            <option value="검토중">검토중</option>
                            <option value="승인완료">승인완료</option>
                            <option value="거부">거부</option>
                        </select>
                        </li>"""
                    e += '<li></li>'
                elif pm_reserv.status == '4':
                    c += f'<li></li>'
                    d += f"""<li>신청마감</li>"""
                    e += f'<li></li>'
                elif pm_reserv.status == '6':
                    c += f'<li style="margin-bottom: 10px">{pm_reserv.school} </li>'
                    d += f"""<li style="margin-bottom: 10px">
                        <select id="status">
                            <option value="신청가능">신청가능</option>
                            <option value="신청대기">신청대기</option>
                            <option value="검토중">검토중</option>
                            <option value="승인완료">승인완료</option>
                            <option value="거부">거부</option>
                        </select>
                        </li>"""
                    e += f"""<li><input type="text" name="reason"></li><li><input type="text" name="reason"></li>"""
            except :
                if day < datetime.today().day:
                    c += f'<li></li>'
                    d += f"""<li>신청대기</li>"""
                    e += f'<li></li>'
                else :
                    c += f'<li></li>'
                    d += f"""<li>신청마감</li>"""
                    e += f'<li></li>'
        if day != 0:
            return f"<tr class='day'><td><span class='date'>{day}일</span></td> <td>{a}</td> <td>{b}</td> <td>{c}</td> <td>{d}</td> <td>{e}</td> </tr>"
        
        return ''

    def formatweek(self, theweek, reservations):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, reservations)
        return f'{week}'

    def formatmonth(self, withyear=True):
        reservations = Reservation.objects.filter(date__year=self.year, date__month=self.month)
        cal = ''
        weekcount = 1
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'<div class="weekcontainer"><h3>{self.month}월 {weekcount}주차</h3>'
            weekcount += 1
            cal += f'<table border="0" cellpadding="0" cellspacint="0", class="weektable">\n'
            cal += f'<th>날짜</th><th>개방</th><th>시간</th><th>상세보기</th><th>신청상태</th><th>사유</th>'
            cal += f'{self.formatweek(week, reservations)}\n'
            cal += f'</table></div>'
        
        return cal
    