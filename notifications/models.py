from django.db import models
from accounts.models import User
import jalali_date

class Notification(models.Model):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='گیرنده',related_name="notifications")
    message = models.CharField(max_length=255 ,verbose_name='پیام')
    created_at = models.DateField(auto_now_add=True ,verbose_name='تاریخ ایجاد')
    time = models.TimeField(auto_now_add=True ,verbose_name='زمان')
    is_read = models.BooleanField(default=False , verbose_name='خوانده شده؟')

    def __str__(self):
        return f"{self.receiver.name} - {self.message}"


    class Meta:
        verbose_name = "اعلان"
        verbose_name_plural = "اعلان ها"



class SMS(models.Model):
    name = models.CharField(max_length=50,
        verbose_name='نام گیرنده')
    receiver = models.CharField(max_length=20,
        verbose_name='شماره همراه گیرنده',
        help_text='09123456789'
    )
    message = models.CharField(
        max_length=255,
        verbose_name='پیام',
        default='https://maps.app.goo.gl/HKXdXNXsLz7B1dNS7'
    )
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='تاریخ ایجاد')

    class Meta:
        ordering = ['-created_at']
        verbose_name = "ارسال پیامک"
        verbose_name_plural = "ارسال پیامک ها"
        
    def __str__(self):
        return f"پیامک برای شماره {self.receiver} ارسال شد"
