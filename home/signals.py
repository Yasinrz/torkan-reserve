from.models import Time
from django.db.models.signals import post_save
from django.dispatch import receiver
from .utils import send_reservation_sms
import jdatetime

@receiver(post_save, sender=Time)
def sms_fixed_reseve(sender, instance, created, **kwargs):
    if created:
        created_at_shamsi = jdatetime.datetime.fromgregorian(
            datetime=instance.fix_reserved_date
        ).strftime("%Y/%m/%d")

        send_reservation_sms(
            instance.request_reservation.user.phone_number,
            instance.request_reservation.user.name,
            created_at_shamsi,
        )