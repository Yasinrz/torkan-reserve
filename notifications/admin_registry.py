from notifications.admin_site import custom_admin_site
from notifications.models import Notification ,SMS
from notifications.admin import NotificationAdmin ,SmsAdmin

custom_admin_site.register(Notification, NotificationAdmin)
custom_admin_site.register(SMS, SmsAdmin)