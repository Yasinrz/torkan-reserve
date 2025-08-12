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



# کارمندان

class StaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default='',verbose_name="کارمند")
    birth_date = models.DateField(verbose_name="تاریخ تولد",null=True , blank=True)
    date_joined = models.DateField(verbose_name="تاریخ پیوستن",auto_now_add=True)

    class Meta:
        verbose_name = "پروفایل کارمند"
        verbose_name_plural = "پروفایل‌های کارمندان"

    def __str__(self):
        return f"{self.user.name} ({self.user.phone_number})"
    


class WorkHourReport(models.Model):

    MONTH_CHOICES = [
        (1, "فروردین"),
        (2, "اردیبهشت"),
        (3, "خرداد"),
        (4, "تیر"),
        (5, "مرداد"),
        (6, "شهریور"),
        (7, "مهر"),
        (8, "آبان"),
        (9, "آذر"),
        (10, "دی"),
        (11, "بهمن"),
        (12, "اسفند"),
    ]

    employee = models.ForeignKey(StaffProfile, on_delete=models.CASCADE, verbose_name="کارمند")
    year = models.IntegerField(choices=[(y, str(y)) for y in range(1400, 1450)], verbose_name="سال")
    month = models.IntegerField(choices=MONTH_CHOICES, verbose_name="ماه")
    duty_hours = models.IntegerField(verbose_name="ساعت موظفی")
    overtime = models.IntegerField(verbose_name="اضافه کاری")

    class Meta:
        verbose_name = "گزارش ساعت کاری"
        verbose_name_plural = "گزارش‌های ساعت کاری"

    def __str__(self):
        return f"{self.employee.user.name} - {self.year}/{self.month}"
    
    def get_month_display_name(self):
        return dict(self.MONTH_CHOICES).get(self.month, "")
    


class Payslip(models.Model):

    MONTH_CHOICES = [
        (1, "فروردین"),
        (2, "اردیبهشت"),
        (3, "خرداد"),
        (4, "تیر"),
        (5, "مرداد"),
        (6, "شهریور"),
        (7, "مهر"),
        (8, "آبان"),
        (9, "آذر"),
        (10, "دی"),
        (11, "بهمن"),
        (12, "اسفند"),
    ]

    employee = models.ForeignKey(StaffProfile, on_delete=models.CASCADE, verbose_name="کارمند")
    year = models.IntegerField(choices=[(y, str(y)) for y in range(1400, 1450)], verbose_name="سال")
    month = models.IntegerField(choices=MONTH_CHOICES, verbose_name="ماه")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    payslip_image = models.FileField(upload_to='payslip/', null=True, blank=True, verbose_name="فیش حقوقی")
    work_hour = models.OneToOneField(WorkHourReport, on_delete=models.CASCADE, verbose_name="گزارش کارکرد ماهانه")

    class Meta:
        verbose_name = "فیش حقوقی"
        verbose_name_plural = "فیش‌های حقوقی"

    def __str__(self):
        return f"فیش {self.employee.user.name} - {self.year}/{self.month}"


class EmployeeTicket(models.Model):
    class TicketType(models.TextChoices):
        LEAVE = "leave", "مرخصی"
        FACILITY = "facility", "تسهیلات"
        ADVANCE = "advance", "مساعده"
        OTHER = "other", "سایر"

    class LeaveType(models.TextChoices):
        SICK = "sick", "استعلاجی"
        ANNUAL = "annual", "استحقاقی"
        UNPAID = "unpaid", "بدون حقوق"

    employee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tickets",
        verbose_name="کارمند",
        help_text="کارمند ایجادکننده این تیکت را انتخاب کنید."
    )
    ticket_type = models.CharField(
        max_length=20,
        choices=TicketType.choices,
        verbose_name="نوع تیکت",
        help_text="نوع درخواست یا مشکل را انتخاب کنید."
    )

    # For Leave
    leave_start = models.DateField(
        null=True, blank=True,
        verbose_name="تاریخ شروع مرخصی",
        help_text="تاریخ شروع مرخصی را وارد کنید."
    )
    leave_end = models.DateField(
        null=True, blank=True,
        verbose_name="تاریخ پایان مرخصی",
        help_text="تاریخ پایان مرخصی را وارد کنید."
    )
    leave_type = models.CharField(
        max_length=20,
        choices=LeaveType.choices,
        null=True, blank=True,
        verbose_name="نوع مرخصی",
        help_text="نوع مرخصی را انتخاب کنید."
    )

    # For Facility
    facility_amount = models.DecimalField(
        max_digits=12, decimal_places=2,
        null=True, blank=True,
        verbose_name="مبلغ تسهیلات",
        help_text="مبلغ تسهیلات مورد نظر را وارد کنید."
    )
    facility_duration_months = models.PositiveIntegerField(
        null=True, blank=True,
        verbose_name="مدت بازپرداخت (ماه)",
        help_text="مدت بازپرداخت تسهیلات به ماه."
    )

    # For Advance
    advance_amount = models.DecimalField(
        max_digits=12, decimal_places=2,
        null=True, blank=True,
        verbose_name="مبلغ مساعده",
        help_text="مبلغ مساعده درخواستی را وارد کنید."
    )

    # Common description for all ticket types
    description = models.TextField(
        null=True, blank=True,
        verbose_name="توضیحات",
        help_text="توضیحات تکمیلی در مورد درخواست خود را وارد کنید."
    )

    # Common fields
    status = models.CharField(
        max_length=20,
        choices=[("open", "باز"), ("in_progress", "در حال بررسی"), ("closed", "بسته شده")],
        default="open",
        verbose_name="وضعیت",
        help_text="وضعیت فعلی تیکت."
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد", help_text="تاریخ ایجاد (سیستمی).")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین بروزرسانی", help_text="تاریخ آخرین بروزرسانی (سیستمی).")

    class Meta:
        ordering = ['created_at']
        verbose_name = " تیکت کارمند"
        verbose_name_plural = " تیکت های کارمندان"

    def __str__(self):
        return f"{self.employee} - {self.get_ticket_type_display()} - {self.status}"


class EmployeeTicketReply(models.Model):
    ticket = models.ForeignKey(
        'EmployeeTicket',
        on_delete=models.CASCADE,
        related_name='replies',
        verbose_name="تیکت مرتبط",
        help_text="تیکتی که این پاسخ مربوط به آن است."
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="نویسنده پاسخ",
        help_text="نویسنده پاسخ (کارمند یا ادمین).",
        editable=False
    )
    message = models.TextField(
        verbose_name="متن پاسخ",
        help_text="متن پاسخ."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد",
        help_text="تاریخ و زمان ایجاد پاسخ."
    )
    is_read = models.BooleanField(
        default=False,
        verbose_name="خوانده شده",
        help_text="آیا این پاسخ توسط گیرنده خوانده شده است؟"
    )

    class Meta:
        ordering = ['created_at']
        verbose_name = "پاسخ تیکت کارمند"
        verbose_name_plural = "پاسخ‌های تیکت کارمندان"

    def __str__(self):
        return f"پاسخ توسط {self.author} در تاریخ {self.created_at.strftime('%Y-%m-%d %H:%M')}"

        