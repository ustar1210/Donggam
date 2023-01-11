from django.db import models
from django.urls import reverse


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
    )
    status = models.CharField(max_length =1, choices=STATUS_CHOICES, null=False, blank=False)

    @property
    def get_html_url(self):
        url = reverse('calender:reservation_edit', args=(self.id,))
        if self.status == '1':
            return f'<a href="{url}">[신청대기]</a>'
        elif self.status == '2':
            return f'<a>[검토중]</a>'
        elif self.status == '3':
            return f'<a>{self.school}</a>'
        elif self.status == '4':
            return f'<a>[신청마감]</a>'
        else :
            if self.time == '10':
                return f'<a href="{url}">[오전 신청가능]</a>'
            else:
                return f'<a href="{url}">[오후 신청가능]</a>'
        
class RegularReservation(models.Model):
    date = models.DateField(null=False, blank=False)
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
        ('0', '신청가능'),
        ('1', '신청대기'),
        ('2', '검토중'),
        ('3', '승인완료'),
        ('4', '신청마감'),
    )
    status = models.CharField(max_length =1, choices=STATUS_CHOICES, null=False, blank=False)
