from django.urls import path, re_path
from . import views

app_name = 'calender'
urlpatterns=[
    re_path(r'^calendar/$', views.CalendarView.as_view(), name='calendar'),
    re_path(r'^reservation/apply/$', views.reservation, name='reservation_new'),
    re_path(r'^reservation/edit/(?P<reservation_id>\d+)/$', views.reservation, name='reservation_edit'),
    re_path(r'^reservation/open/$', views.AdminCalendarView.as_view(), name='calendarAdmin'),
    re_path(f'^reservation/adminsave/$', views.adminsave, name='adminsave'),
    ]