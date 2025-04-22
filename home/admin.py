from django.contrib import admin
from .utils import send_reservation_sms
from django.db import models
from django_jalali.admin.widgets import AdminjDateWidget
from .models import Time , Operation , OperationSetting
from django_jalali.admin.filters import JDateFieldListFilter
from .utils import send_reservation_sms

@admin.register(Time)
class TimeAdmin(admin.ModelAdmin):

    list_display = ('user','shamsi_date','start_session', 'volume', 'unit')
    search_fields = ('user__name', 'user__phone_number')
    list_filter = (('shamsi_date', JDateFieldListFilter),)
    ordering = ('shamsi_date',)
    autocomplete_fields = ('user',)
    formfield_overrides = {
        models.DateField: {'widget': AdminjDateWidget},
    }

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # گرفتن اطلاعات برای پیامک
        phone = obj.user.phone_number
        name = obj.user.name  # یا می‌تونید از first_name و last_name استفاده کنید
        date = obj.shamsi_date.strftime('%Y/%m/%d')

        # ارسال پیامک با استفاده از توکن‌ها
        send_reservation_sms(phone, name, date)


@admin.register(Operation)
class OperationAdmin(admin.ModelAdmin):
    list_display = ['operation_name', ]
    search_fields = ['operation_name',]


@admin.register(OperationSetting)
class OperationSettingAdmin(admin.ModelAdmin):
    list_display = ['Product', 'capacity_materials','unit_capacity','display_calculation', ]
    readonly_fields = ('display_calculation',)


# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ['name', 'phone_number' ]
#     search_fields = ['name',]