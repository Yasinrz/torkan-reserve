from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User , CustomerProfile , SupportTicket ,TicketReply ,Invoice ,StaffProfile ,WorkHourReport ,Payslip , EmployeeTicket,EmployeeTicketReply
from .forms import CustomUserCreationForm, CustomUserChangeForm
from jalali_date.admin import ModelAdminJalaliMixin
from django.utils.html import format_html
from jalali_date import datetime2jalali ,datetime2jalali
from django.utils.translation import gettext_lazy as _
from home.models import Time
from jalali_date import date2jalali




class WorkHourInline(admin.TabularInline):
    model = WorkHourReport
    extra = 0


class PayslipInline(admin.TabularInline):
    model = Payslip
    extra = 0



@admin.register(User)
class UserAdmin(BaseUserAdmin):
    
    list_display = ('phone_number', 'name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('phone_number', 'name')
    ordering = ('phone_number',)
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('اطلاعات شخصی', {'fields': ('name',)}),
        ('دسترسی‌ها', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('تاریخ‌ها', {'fields': ('date_joined',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'name', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

    @admin.display(description=_('datetime joined'))
    def date_joined_jalali(self, obj):
        return datetime2jalali(obj.date_joined).strftime('%Y/%m/%d - %H:%M')
    


@admin.register(WorkHourReport)
class WorkHourReportAdmin(admin.ModelAdmin):
    list_display = ('employee', 'year', 'month', 'duty_hours', 'overtime')
    list_filter = ('year', 'month')
    search_fields = ('employee__phone_number', 'employee__name')

@admin.register(Payslip)
class PayslipAdmin(admin.ModelAdmin):
    list_display = ('employee', 'year', 'month', 'payslip_jalali_date')
    list_filter = ('year', 'month')
    search_fields = ('employee__phone_number', 'employee__name')

    @admin.display(description=_('تاریخ ایجاد'))
    def payslip_jalali_date(self, obj):
        return date2jalali(obj.date_created).strftime('%Y/%m/%d')

@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    inlines = [PayslipInline,WorkHourInline]

    list_display = ('user', 'birth_date', 'staff_joined_jalali_date')
    search_fields = ('employee__name',)

    @admin.display(description=_('تاریخ پیوستن'))
    def staff_joined_jalali_date(self,obj):
        return date2jalali(obj.date_joined).strftime('%Y/%m/%d')




#مشتری ها 

class TicketReplyInline(admin.TabularInline):
    model = TicketReply
    extra = 1
    readonly_fields = ['responder', 'created_at']
    exclude = ['responder']



class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ['title', 'sender', 'support_jalali_date' ,'colored_status']
    inlines = [TicketReplyInline]
    list_filter = ['status']
    readonly_fields = ['status']

    @admin.display(description=_('تاریخ ایجاد'))
    def support_jalali_date(self, obj):
        return date2jalali(obj.created_at).strftime('%Y/%m/%d')


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
    list_display = ['ticket','responder','reply_admin_jalali_date'] 
    list_filter = ['created_at']

    def save_model(self, request, obj, form, change):
        if not obj.responder_id:
            obj.responder = request.user  # مقداردهی responder به کاربر جاری
        super().save_model(request, obj, form, change)

    @admin.display(description=_('تاریخ ایجاد'))
    def reply_admin_jalali_date(self,obj):
        return date2jalali(obj.created_at).strftime('%Y/%m/%d')

admin.site.register(TicketReply,TicketReplyAdmin)



class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['customer','invoice_jalali_date'] 
    list_filter = ['created_date']

    def invoice_preview(self, obj):
        if obj.invoice and obj.invoice.url.lower().endswith(('.png', '.jpg', '.jpeg')):
            return f'<img src="{obj.invoice.url}" width="200" />'
        elif obj.invoice and obj.invoice.url.lower().endswith('.pdf'):
            return f'<a href="{obj.invoice.url}" target="_blank">مشاهده PDF</a>'
        return "فایلی بارگذاری نشده"
    
    invoice_preview.allow_tags = True
    invoice_preview.short_description = 'پیش‌نمایش فاکتور'

    @admin.display(description=_('تاریخ ایجاد'))
    def invoice_jalali_date(self, obj):
        return date2jalali(obj.created_date).strftime('%Y/%m/%d')


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

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(user__is_staff=False)
            

    
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



# Employee Tickets

@admin.register(EmployeeTicket)
class EmployeeTicketAdmin(admin.ModelAdmin):
    list_display = (
        "id", "employee", "ticket_type", "status",
        "leave_start", "leave_end", "facility_amount",
        "advance_amount", "create_employee_ticket_jalali_date"
    )
    list_filter = ("ticket_type", "status", "created_at")
    search_fields = ("employee__username", "employee__first_name", "employee__last_name")

    fieldsets = (
        ("اطلاعات عمومی", {
            "fields": ("employee", "ticket_type", "status", "description")
        }),
        ("مرخصی", {
            "fields": ("leave_start", "leave_end", "leave_type"),
            "classes": ("collapse",)  # جمع‌شونده
        }),
        ("تسهیلات", {
            "fields": ("facility_amount", "facility_duration_months"),
            "classes": ("collapse",)
        }),
        ("مساعده", {
            "fields": ("advance_amount",),
            "classes": ("collapse",)
        }),
        ("زمان‌ها", {
            "fields": ("create_employee_ticket_jalali_date", "updated_at"),
        }),
    )

    readonly_fields = ("create_employee_ticket_jalali_date", "updated_at")

    @admin.display(description=_('تاریخ ایجاد'))
    def create_employee_ticket_jalali_date(self,obj):
        return date2jalali(obj.created_at).strftime('%Y/%m/%d')



    def get_fieldsets(self, request, obj=None):
        """
        بر اساس نوع تیکت، فقط فیلدهای مرتبط را باز نگه می‌دارد.
        """
        fieldsets = super().get_fieldsets(request, obj)
        if obj:
            for title, options in fieldsets:
                if title not in ["اطلاعات عمومی", "زمان‌ها"]:
                    if title != self._get_ticket_type_title(obj.ticket_type):
                        options["classes"] = ("collapse",)
                    else:
                        options.pop("classes", None)
        return fieldsets

    def _get_ticket_type_title(self, ticket_type):
        """
        برگرداندن عنوان فارسی گروه فیلد بر اساس نوع تیکت
        """
        return {
            EmployeeTicket.TicketType.LEAVE: "مرخصی",
            EmployeeTicket.TicketType.FACILITY: "تسهیلات",
            EmployeeTicket.TicketType.ADVANCE: "مساعده",
            EmployeeTicket.TicketType.OTHER: "",  # فقط توضیحات عمومی
        }.get(ticket_type, "")
    


@admin.register(EmployeeTicketReply)
class EmployeeTicketReplyAdmin(admin.ModelAdmin):
    list_display = ("id", "ticket", "author", "replay_employee_jalali_date", "is_read")
    list_filter = ("is_read", "created_at", "author")
    search_fields = ("author__username", "author__first_name", "author__last_name", "ticket__employee__username")
    readonly_fields = ("created_at","author")
    exclude = ['author']
    

    fieldsets = (
        ("اطلاعات پاسخ", {
            "fields": ("ticket","message", "is_read")
        }),
        ("زمان‌ها", {
            "fields": ("created_at",),
        }),
    )

    @admin.display(description=_('تاریخ ایجاد'))
    def replay_employee_jalali_date(self, obj):
        return date2jalali(obj.created_at).strftime('%Y/%m/%d')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user  
        super().save_model(request, obj, form, change)