from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm
from jalali_date.admin import ModelAdminJalaliMixin
from jalali_date import datetime2jalali
from django.utils.translation import gettext_lazy as _


@admin.register(User)
class UserAdmin(ModelAdminJalaliMixin, BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        (None, {'fields': ('name',)}),
        (None, {'fields': ('is_superuser',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'name', 'password1', 'password2', 'is_superuser',),
        }),
    )
    list_display = ('phone_number', 'name', 'is_superuser', 'date_joined_jalali',)
    search_fields = ('phone_number', 'name')
    ordering = ('date_joined',)
    readonly_fields = ['is_superuser']

    @admin.display(description=_('datetime joined'))
    def date_joined_jalali(self, obj):
        return datetime2jalali(obj.date_joined).strftime('%Y/%m/%d - %H:%M')
