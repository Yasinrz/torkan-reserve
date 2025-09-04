from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import CustomerProfile ,StaffProfile ,EmployeeTicketReply , EmployeeTicket ,SupportTicket
from . utils import customer_ticket , employee_ticket
import jdatetime


User = get_user_model()


@receiver(post_save, sender=User)
def create_customer_profile(sender, instance, created, **kwargs):
    if created:
        CustomerProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def create_staff_profile(sender, instance, created, **kwargs):
    
    if created and instance.is_staff:
        StaffProfile.objects.create(user=instance)
    else:
        
        if instance.is_staff and not hasattr(instance, 'staffprofile'):
            StaffProfile.objects.create(user=instance)
        
        elif not instance.is_staff and hasattr(instance, 'staffprofile'):
            instance.staffprofile.delete()


@receiver(post_save, sender=EmployeeTicketReply)
def update_ticket_status(sender, instance, created, **kwargs):
    if created and instance.author.is_staff:
        instance.ticket.status = 'answered'
        instance.ticket.save()


@receiver(post_save, sender=SupportTicket)
def cuetomer_ticket_sms(sender, instance, created, **kwargs):
    if created:
        # تبدیل به شمسی
        created_at_shamsi = jdatetime.datetime.fromgregorian(
            datetime=instance.created_at
        ).strftime("%Y/%m/%d")


        customer_ticket(
            instance.sender.name,
            created_at_shamsi,
            instance.sender.phone_number,
        )



@receiver(post_save, sender=EmployeeTicket)
def employee_ticket_sms(sender, instance, created, **kwargs):
    if created:
        
        employee_ticket(
            instance.employee.name,
            instance.get_ticket_type_display(),
            instance.employee.phone_number,
        )
        
        
    