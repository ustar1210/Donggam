from django.db import models
from django.urls import reverse

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    @property
    def get_html_url(self):
        url = reverse('calender:event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'

class Reservation(models.Model):
    date = models.DateField(null=False, blank=False)
    TIME_CHOICES = (
        ('10', '10:00'),
        ('14', '14:00'),
    )
    time = models.CharField(max_length=2, choices=TIME_CHOICES, null=False, blank=False)
    AGE_CHOICES = (
        ('u', '14세이상'),
        ('d', '14세미만'),
    )
    age = models.CharField(max_length=1, choices=AGE_CHOICES, null=False, blank=False)
    name = models.CharField(max_length=12, null=False, blank=False)
    email = models.CharField(max_length=50, null=False, blank=False)
    school = models.CharField(max_length=30, null=False, blank=False)
    GRADE_CHOICES = (
        ('1', '1학년'),
        ('2', '2학년'),
        ('3', '3학년'),
        ('n', '기타'),
    )
    grade = models.CharField(max_length=1, choices=GRADE_CHOICES, null=False, blank=False)
    headcount = models.IntegerField(null=False, blank=False)
    phone = models.CharField(max_length=11, null=False, blank=False)
    motivation = models.TextField(max_length=200, null=False, blank=False)
    request = models.TextField(max_length=200, null=True, blank=True)
    STATUS_CHOICES = (
        ('0', '신청대기'),
        ('1', '검토중'),
        ('2', '승인완료'),
    )
    status = models.CharField(max_length =1, choices=STATUS_CHOICES, null=False, blank=False)

    @property
    def get_html_url(self):
        url = reverse('calender:reservation_edit', args=(self.id,))
        if self.status == '0':
            return f'<a href="{url}"> [신청대기] </a>'
        elif self.status == '1':
            return f'<a> [검토중] </a>'
        else:
            return f'<a> {self.school} </a>'
        