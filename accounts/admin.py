from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User , CustomerProfile , SupportTicket ,TicketReply ,Invoice
from .forms import CustomUserCreationForm, CustomUserChangeForm
from jalali_date.admin import ModelAdminJalaliMixin
from django.utils.html import format_html
from jalali_date import datetime2jalali
from django.utils.translation import gettext_lazy as _
from home.models import Time


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



class TicketReplyInline(admin.TabularInline):
    model = TicketReply
    extra = 1
    readonly_fields = ['responder', 'created_at']
    exclude = ['responder']


class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ['title', 'sender', 'created_at' ,'colored_status']
    inlines = [TicketReplyInline]
    list_filter = ['status']
    readonly_fields = ['status']


    def colored_status(self,obj):
        if obj.status=='answered':
            background = "#32CD32"
            text = 'پاسخ داده شده'
        else:
            background = "#FF0000"
            text = 'پاسخ داده نشده'
        return format_html(
            '<div style="background-color: {}; padding:4px 8px; border-radius:5px; text-align:center;">{}</div>',
            background,
            text
        )
    
    colored_status.short_description = 'وضعیت'
    

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if not instance.pk:
                instance.responder = request.user 
                instance.save()
                instance.ticket.status = 'answered'  
                instance.ticket.save()
            else:
                instance.save()
        formset.save_m2m()



admin.site.register(SupportTicket, SupportTicketAdmin)

class TicketReplyAdmin(admin.ModelAdmin):
    list_display = ['ticket','responder','created_at'] 
    list_filter = ['created_at']
admin.site.register(TicketReply,TicketReplyAdmin)


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['customer','created_date'] 
    list_filter = ['created_date']

    def invoice_preview(self, obj):
        if obj.invoice and obj.invoice.url.lower().endswith(('.png', '.jpg', '.jpeg')):
            return f'<img src="{obj.invoice.url}" width="200" />'
        elif obj.invoice and obj.invoice.url.lower().endswith('.pdf'):
            return f'<a href="{obj.invoice.url}" target="_blank">مشاهده PDF</a>'
        return "فایلی بارگذاری نشده"
    
    invoice_preview.allow_tags = True
    invoice_preview.short_description = 'پیش‌نمایش فاکتور'

admin.site.register(Invoice,InvoiceAdmin)    

class InvoiceInline(admin.TabularInline):
    model = Invoice
    extra = 0
    readonly_fields = ('invoice', 'created_date')
    can_delete = False
    
    def has_add_permission(self, request, obj=None):
        return False

@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ['user',]
    readonly_fields = ['show_reserve_history','show_tikets']
    inlines = [InvoiceInline]
    

    def show_reserve_history(self,obj):
        times = Time.objects.filter(request_reservation__user=obj.user).order_by('-fix_reserved_date')
        if not times.exists():
            return "not reserve"
        return "<br>".join(
            [f"{t.fix_reserved_date.strftime('%Y-%m-%d %H:%M')}" for t in times]
        )
    show_reserve_history.short_description = "تاریخچه رزروها"
    show_reserve_history.allow_tags = True

    def show_tikets(self,obj):
        tikets = SupportTicket.objects.filter(sender=obj.user).order_by('-created_at')
        if not tikets.exists():
            return "تیکتی وجود ندارد"
        return "<br>".join([
            f"{t.created_at.strftime('%Y-%m-%d %H:%M')} - {t.title}" for t in tikets
        ])
    show_tikets.short_description = "تاریخچه تیکت ها"
    show_tikets.allow_tags = True
