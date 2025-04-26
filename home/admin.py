from django.contrib import admin
from django.db import models
from django_jalali.admin.widgets import AdminjDateWidget
from .models import Time, Operation, OperationSetting
from django_jalali.admin.filters import JDateFieldListFilter
from .utils import send_reservation_sms


@admin.register(Time)
class TimeAdmin(admin.ModelAdmin):
    list_display = ('request_reservation', 'shamsi_date', 'start_session', 'volume', 'unit')
    search_fields = ('request_reservation__user__name', 'request_reservation__user__phone_number')
    list_filter = (('shamsi_date', JDateFieldListFilter),)
    ordering = ('shamsi_date',)
    readonly_fields = ('date_time_reserved',)
    # autocomplete_fields = ('request_reservation_user',)
    formfield_overrides = {
        models.DateField: {'widget': AdminjDateWidget},
    }

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # get data to send SMS
        phone = obj.request_reservation.user.phone_number
        name = obj.request_reservation.user.name
        date = obj.shamsi_date.strftime('%Y/%m/%d')

        send_reservation_sms(phone, name, date)


@admin.register(Operation)
class OperationAdmin(admin.ModelAdmin):
    list_display = ['operation_name', ]
    search_fields = ['operation_name', ]


@admin.register(OperationSetting)
class OperationSettingAdmin(admin.ModelAdmin):
    list_display = ['Product', 'capacity_materials', 'unit_capacity', 'display_calculation', ]
    readonly_fields = ('display_calculation',)
