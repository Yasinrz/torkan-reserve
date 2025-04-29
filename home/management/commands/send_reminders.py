from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import jdatetime
from home.models import Time
from home.utils import send_reminder_sms  # اگر send_reminder_sms در جای دیگری تعریف شده


class Command(BaseCommand):
    help = "Send reminder SMS to users 2 days before their appointment"

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        target_date = today + timedelta(days=2)

        # فقط برای نمایش شمسی
        target_date_shamsi = jdatetime.date.fromgregorian(date=target_date).strftime('%Y-%m-%d')
        self.stdout.write(
            f"📅 Today (Miladi): {today}, Target Date (Miladi): {target_date}, Target Date (Shamsi): {target_date_shamsi}"
        )

        # بررسی و تصحیح داده‌های اشتباه در دیتابیس (shamsi_date که به جای میلادی، شمسی ذخیره شده‌اند)
        for t in Time.objects.all():
            sd = t.shamsi_date
            if sd and sd.year < 1600:  # اگر شمسی به اشتباه در فیلد میلادی ذخیره شده
                try:
                    shamsi = jdatetime.date(sd.year, sd.month, sd.day)
                    miladi = shamsi.togregorian()
                    t.shamsi_date = miladi
                    t.save()
                    print(f"✅ تاریخ {shamsi} تبدیل شد به {miladi}")
                except Exception as e:
                    print(f"⚠️ خطا برای id={t.id}: {e}")

        # فیلتر نهایی پس از تصحیح تاریخ‌ها
        appointments = Time.objects.filter(shamsi_date=target_date)
        self.stdout.write(f"🔍 تعداد نوبت‌های یافت‌شده برای {target_date}: {appointments.count()}")

        if not appointments.exists():
            self.stdout.write("⚠️ هیچ نوبتی برای این تاریخ پیدا نشد.")
            return

        # ارسال پیامک برای هر نوبت
        for appointment in appointments:
            user = appointment.request_reservation.user
            phone = user.phone_number
            date = jdatetime.date.fromgregorian(date=appointment.shamsi_date).strftime('%Y/%m/%d')
            time = appointment.start_session.strftime('%H:%M')

            result = send_reminder_sms(phone, date, time)

            if isinstance(result, dict) and "error" not in result:
                print(f"✅ پیامک برای {phone} ارسال شد ({date} {time})")
            else:
                print(f"❌ ارسال پیامک برای {phone} با خطا مواجه شد: {result}")
