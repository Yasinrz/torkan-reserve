from django.contrib import admin
from django.db import models
from django_jalali.admin.widgets import AdminjDateWidget
from .models import Time, Operation, OperationSetting, RequestReservation
from django_jalali.admin.filters import JDateFieldListFilter
from jalali_date.admin import ModelAdminJalaliMixin
from jalali_date import date2jalali
from .utils import send_reservation_sms
from .forms import RequestReservationForm


@admin.register(Time)
class TimeAdmin(admin.ModelAdmin):
    list_display = ('request_reservation', 'shamsi_date', 'start_session', 'volume', 'unit')
    search_fields = ('request_reservation__user__name', 'request_reservation__user__phone_number')
    list_filter = (('shamsi_date', JDateFieldListFilter),)
    ordering = ('shamsi_date',)
    readonly_fields = ('date_time_reserved',)
    autocomplete_fields = ('request_reservation',)
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


@admin.register(RequestReservation)
class RequestReservationAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['user', 'datetime_created', 'suggested_reservation_date', 'status', ]
    search_fields = ['user__name', 'user__phone_number']
    ordering = ['-datetime_created', ]

    @admin.display(description='suggested_reservation_date')
    def get_jalali_date(self, obj):
        return date2jalali(obj.date).strftime('%Y/%m/%d')
