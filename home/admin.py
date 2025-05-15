from django.contrib import admin
import jdatetime
from jalali_date.widgets import AdminJalaliDateWidget
from django.db import models
from django_jalali.admin.widgets import AdminjDateWidget
from .models import Time, Operation, OperationSetting, RequestReservation
from django_jalali.admin.filters import JDateFieldListFilter
from jalali_date.admin import ModelAdminJalaliMixin
from jalali_date import date2jalali
from .models import Time, Operation, OperationSetting, RequestReservation
from .utils import send_reservation_sms


@admin.register(Time)
class TimeAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('request_reservation', 'fix_reserved_date', 'start_session', 'volume', 'unit')
    search_fields = ('request_reservation__user__name', 'request_reservation__user__phone_number')
    ordering = ('-fix_reserved_date',)
    readonly_fields = ('date_time_created',)
    autocomplete_fields = ('request_reservation',)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # get data to send SMS
        phone = obj.request_reservation.user.phone_number
        name = obj.request_reservation.user.name
        miladi_date = form.cleaned_data['fix_reserved_date']
        shamsi_date = jdatetime.date.fromgregorian(date=miladi_date)
        date = shamsi_date.strftime('%Y/%m/%d')


        send_reservation_sms(phone, name, date)


    @admin.display(description='fixed_reserved_date')
    def get_jalali_date(self, obj):
        return date2jalali(obj.date).strftime('%Y/%m/%d')


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
