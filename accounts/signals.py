from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import CustomerProfile ,StaffProfile

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