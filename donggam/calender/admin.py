from django.contrib import admin
from calender.models import Place, Reservation, RegularReservation, RegularDate
from django.shortcuts import get_object_or_404
from django.utils.safestring import mark_safe

admin.site.register(Place)
admin.site.register(RegularDate)

def group_confirm(modeladmin, request, queryset):
    place = get_object_or_404(Place, name='정각원 앞 백년비')
    queryset.update(status = '3', place = place)

group_confirm.short_description = '선택한 단체투어를 승인합니다.'

class GroupAdmin(admin.ModelAdmin):
    list_display = ['datetime', 'school', 'name', 'status']
    actions = [group_confirm]

    def datetime(self, reservation):
        return mark_safe('<u>{}</u>'.format(reservation))
    datetime.short_description = 'datetime'

admin.site.register(Reservation, GroupAdmin)

def regular_confirm(modeladmin, request, queryset):
    place = get_object_or_404(Place, name='팔정도 코끼리상 앞')
    queryset.update(status = '2', place = place)

regular_confirm.short_description = '선택한 정기투어를 승인합니다.'

class RegularAdmin(admin.ModelAdmin):
    list_display = ['datetime', 'school', 'name', 'status']
    actions = [regular_confirm]

    def datetime(self, regular_reservation):
        return mark_safe('<u>{}</u>'.format(regular_reservation))
    datetime.short_description = 'datetime'

admin.site.register(RegularReservation, RegularAdmin)