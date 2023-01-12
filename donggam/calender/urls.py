from django.urls import path, re_path
from . import views

app_name = 'calender'
urlpatterns=[
    path('', views.index, name='index'),
    path('group_notice/', views.group_notice, name='group_notice'),
    re_path(r'^calendar/$', views.CalendarView.as_view(), name='calendar'),
    re_path(r'^reservation/check/(?P<reservation_id>\d+)$', views.reservationCheck, name='reservation_check'),
    re_path(r'^reservation/pw/(?P<reservation_id>\d+)/$', views.password, name='password'),
    re_path(r'^reservation/pw/(?P<reservation_id>\d+)/check/$', views.pw_check, name='pw_check'),
    #re_path(r'^reservation/apply/$', views.reservation, name='reservation_new'),
    re_path(r'^reservation/edit/(?P<reservation_id>\d+)/$', views.reservation, name='reservation_edit'),
    path('regular_list/', views.regular_list, name='regular_list'),
    path('regular_form/', views.regular_form, name='regular_form'),
    ]