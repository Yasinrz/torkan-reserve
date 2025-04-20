from django.contrib import admin
from django.db import models
from django_jalali.admin.widgets import AdminjDateWidget
from .models import Time , Operation , OperationSetting
from django_jalali.admin.filters import JDateFieldListFilter

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