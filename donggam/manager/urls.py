from django.urls import path, re_path
from . import views

app_name = 'manager'
urlpatterns=[
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    re_path(r'^calendar/open/$', views.AdminCalendarView.as_view(), name='calendarAdmin'),
    re_path(f'^calendar/adminsave/$', views.adminsave, name='adminsave'),
    ]