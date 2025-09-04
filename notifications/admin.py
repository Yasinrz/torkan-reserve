from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("message", "receiver", "created_at", 'time',"is_read")

    class Media:
        js = ("notifications/js/notifications.js",)
                