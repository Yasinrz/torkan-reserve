from django.contrib import admin
from .models import Notification , SMS
from jalali_date import date2jalali
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("message", "receiver", "created_at", 'time',"is_read")

    # class Media:
    #     js = ("notifications/js/notifications.js",)
                

@admin.register(SMS)
class SmsAdmin(admin.ModelAdmin):
    list_display = ['receiver', 'message', 'created_at']
    list_filter = ['created_at']

    @admin.display(description='تاریخ ایجاد')
    def get_shamsi(self,obj):
        return date2jalali(obj.created_at).strftime('%Y/%m/%d')