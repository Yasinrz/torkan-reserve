from django.contrib import admin
import jdatetime
from jalali_date.admin import ModelAdminJalaliMixin, StackedInlineJalaliMixin
from jalali_date import date2jalali, datetime2jalali
from .models import Time, Operation, OperationSetting, RequestReservation
from .utils import send_reservation_sms
from django.utils.translation import gettext_lazy as _


@admin.register(Time)
class TimeAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = (
    'id', 'trans_request_reservation_date', 'format_date', 'start_session', 'volume', 'unit', 'datetime_saved')
    search_fields = ('request_reservation__user__name', 'request_reservation__user__phone_number')
    ordering = ('-fix_reserved_date',)
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

    @admin.display(description=_('Reservation date'))
    def format_date(self, obj):
        return date2jalali(obj.fix_reserved_date).strftime('%Y/%m/%d')

    @admin.display(description=_('Request reservation date'))
    def trans_request_reservation_date(self, obj):
        return obj.request_reservation.user

    @admin.display(description=_('datetime saved'))
    def datetime_saved(self, obj):
        return datetime2jalali(obj.request_reservation.datetime_created).strftime('%Y/%m/%d - %H:%M')


@admin.register(Operation)
class OperationAdmin(admin.ModelAdmin):
    list_display = ['operation_name', ]
    search_fields = ['operation_name', ]


@admin.register(OperationSetting)
class OperationSettingAdmin(admin.ModelAdmin):
    list_display = ['Product', 'capacity_materials', 'unit_capacity', 'display_calculation', ]
    readonly_fields = ('display_calculation',)


# StackedInline part in admin for RequestReservation model
class TimeInline(StackedInlineJalaliMixin, admin.TabularInline):
    model = Time


@admin.register(RequestReservation)
class RequestReservationAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['id', 'user', 'datetime_created_jalali', 'suggested_jalali_date', 'status', ]
    search_fields = ['user__name', 'user__phone_number']
    ordering = ['-datetime_created', ]
    readonly_fields = ['user']
    inlines = [TimeInline]

    @admin.display(description=_('suggested_reservation_date'))
    def suggested_jalali_date(self, obj):
        return date2jalali(obj.suggested_reservation_date).strftime('%Y/%m/%d')

    @admin.display(description=_('datetime_created'))
    def datetime_created_jalali(self, obj):
        return date2jalali(obj.datetime_created.date()).strftime('%Y/%m/%d')
