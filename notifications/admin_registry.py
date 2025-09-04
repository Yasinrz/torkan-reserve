from notifications.admin_site import custom_admin_site
from notifications.models import Notification
from notifications.admin import NotificationAdmin

custom_admin_site.register(Notification, NotificationAdmin)
