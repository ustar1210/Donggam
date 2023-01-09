from django.urls import path, re_path
from . import views

app_name = 'calender'
urlpatterns=[
    re_path(r'^calendar/$', views.CalendarView.as_view(), name='calendar'),
    re_path(r'^event/new/$', views.event, name='event_new'),
    re_path(r'^event/edit/(?P<event_id>\d+)/$', views.event, name='event_edit'),
    re_path(r'^reservation/new/(?P<datetime>\d)/$', views.reservation, name='reservation_new'),
    re_path(r'^reservation/edit/(?P<reservation_id>\d+)/$', views.reservation, name='reservation_edit'),
    ]