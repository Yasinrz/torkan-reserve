from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

class UserManager(BaseUserManager):
    def create_user(self, phone_number, name, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("Users must have a phone number")
        if not name:
            raise ValueError("Users must have a name")
        user = self.model(phone_number=phone_number, name=name, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if not password:
            raise ValueError("Superuser must have a password")
        if not phone_number:
            raise ValueError("Superuser must have a phone number")

        return self.create_user(phone_number, name='Admin', password=password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=20, unique=True,verbose_name=_('phone number'))
    name = models.CharField(max_length=100,verbose_name=_('First and last name'))
    is_active = models.BooleanField(default=True , verbose_name=_('is active ?'))
    is_staff = models.BooleanField(default=False, verbose_name=_('is staff ?'))
    is_superuser = models.BooleanField(default=False , verbose_name=_('is superuser ?'))
    date_joined = models.DateTimeField(default=timezone.now ,verbose_name=_('date joined'))

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"    {_('user')}  {self.name}  ,  {self.phone_number}"
    

User = get_user_model()

class SupportTicket(models.Model):
    STATUS_CHOICES =[
        ('pending','در انتظار پاسخ'),
        ('answered','پاسخ داده شده'),
    ]

    sender = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر ارسال‌کننده")
    title = models.CharField(max_length=100, verbose_name="عنوان")
    message = models.TextField(verbose_name="پیام")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')


    def __str__(self):
        return f"{self.sender.name} - {self.title}"
    
    @property
    def is_answered(self):
        return self.replies.exists()

    class Meta:
        verbose_name = "تیکت مشتری"
        verbose_name_plural = "تیکت‌های مشتریان"


class TicketReply(models.Model):
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name="replies")
    responder = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name="پاسخ‌دهنده"
                ,editable=False)
    message = models.TextField(verbose_name="پاسخ")
    created_at = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        # ذخیره پاسخ
        super().save(*args, **kwargs)
        # وضعیت تیکت را آپدیت کن
        if self.responder.is_staff:
            self.ticket.status = 'answered'



    def __str__(self):
        return f"پاسخ به تیکت {self.ticket.sender} توسط {self.responder.name}"
    
    class Meta:
        verbose_name = "پاسخ پشتیبانی"
        verbose_name_plural = "پاسخ های پشتیبانی"



class CustomerProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر", editable=False)
    
    def __str__(self):
        return f"پروفایل {self.user.name}"

    class Meta:
        verbose_name = "پروفایل مشتری"
        verbose_name_plural = "پروفایل‌های مشتری"

class Invoice(models.Model):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, verbose_name="کاربر")
    invoice = models.FileField(upload_to='invoices/', null=True, blank=True, verbose_name="فاکتور")
    created_date = models.DateTimeField(auto_now_add=True)


 