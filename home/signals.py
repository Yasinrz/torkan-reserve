from.models import Time
from django.db.models.signals import post_save
from django.dispatch import receiver
from .utils import send_reservation_sms
import jdatetime
from config.settings import DEBUG

@receiver(post_save, sender=Time)
def sms_fixed_reseve(sender, instance, created, **kwargs):
    if created and not DEBUG:
        created_at_shamsi = jdatetime.datetime.fromgregorian(
            datetime=instance.fix_reserved_date
        ).strftime("%Y/%m/%d")

        send_reservation_sms(
            instance.request_reservation.user.phone_number,
            instance.request_reservation.user.name,
            created_at_shamsi,
        )
    if created:
        print("$---- send fixed reservation time ----$\n")
    else:
        print("$---- Not send fixed reservation time ----$\n")