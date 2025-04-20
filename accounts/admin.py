from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        (_('Personal info'), {'fields': ('name',)}),
        (_('Permissions'), {'fields': ('is_staff', 'is_superuser',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'name', 'password1', 'password2', 'is_superuser', 'is_staff',),
        }),
    )
    list_display = ('phone_number', 'name', 'is_active', 'date_joined',)
    search_fields = ('phone_number', 'name')
    ordering = ('date_joined',)
