from django.urls import path, re_path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'manager'
urlpatterns=[
    path('', views.manager_index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='manager/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    re_path(r'^calendar/open/$', views.AdminCalendarView.as_view(), name='calendarAdmin'),
    re_path(f'^calendar/adminsave/$', views.admin_save, name='adminsave'),
    re_path(r'^reservation/group/(?P<reservation_id>\d+)$', views.group_form, name='group_form'),
    ]