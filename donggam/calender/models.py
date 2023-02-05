from django.db import models
from django.urls import reverse

class Place(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.name

class Reservation(models.Model):
    date = models.DateField(null=False, blank=False)
    TIME_CHOICES = (
        ('10', '10:00'),
        ('14', '14:00'),
    )
    time = models.CharField(max_length=2, choices=TIME_CHOICES, null=False, blank=False)
    name = models.CharField(max_length=12, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    school = models.CharField(max_length=30, null=True, blank=True)
    GRADE_CHOICES = (
        ('1', '1학년'),
        ('2', '2학년'),
        ('3', '3학년'),
        ('n', '기타'),
    )
    grade = models.CharField(max_length=1, choices=GRADE_CHOICES, null=True, blank=True)
    MAJOR_CHOICES = (
        (0, '공통'),
        (1, '문과'),
        (2, '이과'),
    )
    major = models.IntegerField(choices=MAJOR_CHOICES, null=True, blank=True)
    bus = models.IntegerField(null=True, blank=True)
    headcount = models.IntegerField(null=True, blank=True)
    LENGTH_CHOICES = (
        (6, '60분'),
        (9, '90분'),
    )
    length = models.IntegerField(choices=LENGTH_CHOICES, null=True, blank=True)
    memo = models.TextField(max_length=200, null=True, blank=True)
    STATUS_CHOICES = (
        ('0', '신청가능'),
        ('1', '신청대기'),
        ('2', '검토중'),
        ('3', '승인완료'),
        ('4', '신청마감'),
        ('5', '휴일'),
    )
    status = models.CharField(max_length =1, choices=STATUS_CHOICES, null=False, blank=False)
    place = models.ForeignKey(Place, on_delete=models.SET_NULL, null=True, blank=True)
    admin_comment = models.TextField(max_length=200, null=True, blank=True)
    
    @property
    def get_html_url(self):
        url = reverse('calender:reservation_check', args=(self.id,))
        if self.status == '1':
            return f'<a class="schoolAply" href="{url}">[신청대기]</a>'
        elif self.status == '2':
            return f'<a class="schoolAply" href="{url}">[검토중]</a>'
        elif self.status == '3':
            return f'<a class="schoolAply" href="{url}">{self.school}</a>'
        elif self.status == '4':
            return f'<a class="endAply" >[신청마감]</a>'
        elif self.status == '5':
            return f'<a class="holiday">휴일</a>'
        else :
            url = reverse('calender:reservation_edit', args=(self.id,))
            if self.time == '10':
                return f'<a class="waitAply" href="{url}">[오전 신청가능]</a>'
            else:
                return f'<a class="waitAply" href="{url}">[오후 신청가능]</a>'
    
    @property
    def get_admin_url(self):
        url = reverse('manager:group_form', args=(self.id,))
        if self.status == '1':
            return f'<a class="schoolAply" href="{url}">[신청대기]</a>'
        elif self.status == '2':
            return f'<a class="schoolAply" href="{url}">[검토중]</a>'
        elif self.status == '3':
            return f'<a class="schoolAply" href="{url}">{self.school}</a>'
        elif self.status == '4':
            return f'<a class="endAply" style="color : #585757">[신청마감]</a>'
        elif self.status == '5':
            return f'<a class="holiday">휴일</a>'
        else :
            if self.time == '10':
                return f'<a class="waitAply" style="color: #0085FF;">[오전 신청가능]</a>'
            else:
                return f'<a class="waitAply" style="color: #0085FF;">[오후 신청가능]</a>'

    def __str__(self):
        datetime = str(self.date)+' / '+self.time+':00'
        if self.status == '1':
            status = '[신청대기]'
        elif self.status == '2':
            status =  '[검토중]'
        elif self.status == '3':
            status = '[승인완료]'
        elif self.status == '4':
            status = '[신청마감]'
        elif self.status == '5':
            return str(self.date) + ' / 휴일'
        else :
            if self.time == '10':
                status = '[오전 신청가능]'
            else:
                status = '[오후 신청가능]'
        return datetime + status
        

class RegularDate(models.Model):
    date = models.DateField(null=False, blank=True)

    def __str__(self):
        days = ['월', '화', '수', '목', '금', '토', '일']
        day = self.date.weekday()
        return str(self.date.month) + '월 ' + str(self.date.day) + '일(' + days[day] + ')'

        
class RegularReservation(models.Model):
    date = models.ForeignKey(RegularDate, on_delete=models.SET_NULL, null=True, blank=True)
    AGE_CHOICES = (
        ('u', '14세이상'),
        ('d', '14세미만'),
    )
    age = models.CharField(max_length=1, choices=AGE_CHOICES, null=True, blank=True)
    parent_name = models.CharField(max_length=12, null=True, blank=True)
    parent_phone = models.CharField(max_length=15, null=True, blank=True)
    name = models.CharField(max_length=12, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    school = models.CharField(max_length=30, null=True, blank=True)
    GRADE_CHOICES = (
        ('1', '1학년'),
        ('2', '2학년'),
        ('3', '3학년'),
        ('n', '기타'),
    )
    grade = models.CharField(max_length=1, choices=GRADE_CHOICES, null=True, blank=True)
    headcount = models.IntegerField(null=True, blank=True)
    motivation = models.TextField(max_length=200, null=True, blank=True)
    request = models.TextField(max_length=200, null=True, blank=True)
    STATUS_CHOICES = (
        ('1', '검토중'),
        ('2', '승인완료'),
        ('3', '재확인 필요'),
    )
    status = models.CharField(max_length =1, choices=STATUS_CHOICES, null=False, blank=False)
    place = models.ForeignKey(Place, on_delete=models.SET_NULL, null=True, blank=True)
    admin_comment = models.TextField(max_length=200, null=True, blank=True)
    created_at = models.DateField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name + '님의 정기 캠퍼스투어 신청'