# notification/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification
from accounts.models import User,SupportTicket,EmployeeTicket,Suggestion
from home.models import RequestReservation

@receiver(post_save, sender=SupportTicket)
def create_ticket_notification(sender, instance, created, **kwargs):
    print(f"Signal triggered for SupportTicket: {instance.id}, created: {created}")
    if created: 
        admin_user = User.objects.filter(is_superuser=True).first()
        if admin_user:
            notif = Notification.objects.create(
                receiver=admin_user,
                message=f"کاربر {instance.sender.name} یک تیکت جدید ثبت کرد."
            )
            

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "admins",
                {
                    "type": "send_notification",
                    "message": notif.message,
                    "ticket_url": f"/admin/accounts/supportticketproxy/{instance.id}/change/"
                }
            )



@receiver(post_save, sender=EmployeeTicket)
def create_employee_ticket_notification(sender, instance, created, **kwargs):
    if not created:
        return
    
    admins = User.objects.filter(is_superuser=True)
    channel_layer = get_channel_layer()

    for admin_user in admins:
        notif = Notification.objects.create(
            receiver=admin_user,
            message=f"کارمند {instance.employee.name} درخواست {instance.get_ticket_type_display()} دارد."
        )

        async_to_sync(channel_layer.group_send)(
            "admins",
            {
                "type": "send_notification",
                "message": notif.message,
                "ticket_url": f"/admin/accounts/employeeticketproxy/{instance.id}/change/",
                "notif_type": "employee_ticket"
            }
        )


@receiver(post_save,sender=RequestReservation)
def create_request_reseve(sender , instance, created, **kwargs):
    if not created:
        return
    
    admins = User.objects.filter(is_superuser=True)
    channel_layer = get_channel_layer()

    for admin_user in admins:
        notif = Notification.objects.create(
            receiver=admin_user,
            message = f"کاربر {instance.request_reservation.user.name} درخواست رزرو نوبت در تاریخ {instance.suggested_reservation_date} دارد.",
        )

        async_to_sync(channel_layer.group_send)(
            "admins",
            {
                "type": "send_notification",
                "message": notif.message,
                "ticket_url": f"/admin/accounts/employeeticketproxy/{instance.id}/change/",
                "notif_type": "employee_ticket"
            }
        )

@receiver(post_save , sender=Suggestion)
def create_suggestion_notification(sender ,instance ,created ,**kwargs):
    if not created:
        return
    
    admins = User.objects.filter(is_superuser=True)
    channel_layer = get_channel_layer()

    for admin_user in admins:
        notif =  Notification.objects.create(
            receiver=admin_user,
            message=f"{instance.get_user_type_display()} {instance.user.name} پیشنهاد خود را ثبت کرد.",
        )

        async_to_sync(channel_layer.group_send)(
            "admins",
            {
                "type": "send_notification",
                "message": notif.message,
                "ticket_url": f"/admin/accounts/suggestion/{instance.id}/change/",
            }
        )