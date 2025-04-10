from re import search
from django.db import models
from xml.dom import ValidationErr
from django.core.exceptions import ValidationError
import jdatetime
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.

class Operation(models.Model):
    operation_name = models.CharField(max_length=50, verbose_name='نام عملیات ')

    def __str__(self):
        return self.operation_name


class OperationSetting(models.Model):
    Unit = [
        ("gal", "گالن"),
        ("but", "بوته",),
        ("kilo", "کیلو گرم")
    ]

    operation = models.ForeignKey(Operation, on_delete=models.CASCADE, verbose_name='نوع عملیات', null=True, blank=True)
    unit_capacity = models.CharField(choices=Unit, max_length=10, null=True, blank=True, verbose_name='واحد محاسبه ')
    capacity = models.IntegerField(default=0, verbose_name='تعداد کوره برای انجام این عملیات ')
    capacity_materials = models.IntegerField(default=1, verbose_name='حجم مواد')
    zamini = models.BooleanField(verbose_name='ذوب زمینی دارد؟', default=False)
    Product = models.CharField(max_length=20, null=True, blank=True, verbose_name='نام محصول')

    # برای مثال تعداد هر ظرفیت برابر 5 بوته است

    def calculation(self):
        Cap = 0
        Finaltime = 0
        kilo = 0

        if self.unit_capacity == 'but':
            galen = self.capacity_materials * 2
            kilo = galen * 17

            while kilo > 0:
                Cap += 1
                kilo -= 150

            Finaltime = Cap * 2


        elif self.unit_capacity == 'gal':
            galen = self.capacity_materials
            kilo = galen * 17

            while kilo > 0:
                Cap += 1
                kilo -= 150

            Finaltime = Cap * 2


        else:
            kilo = self.capacity_materials
            while kilo > 0:
                Cap += 1
                kilo -= 150

            Finaltime = Cap * 2

        return f"مدت زمان ذوب این مواد {Finaltime} ساعت میباشد"

    def display_calculation(self):
        return self.calculation()

    display_calculation.short_description = 'مدت زمان ذوب'  # عنوان ستون در ادمین



class User(models.Model):
    name = models.CharField(max_length=50, verbose_name='نام و نام خانوادگی ')
    phone_number = models.CharField(max_length=11, verbose_name=' شماره تلفن همراه ')

    def __str__(self):
        return f" کاربر {self.name} - {self.phone_number}"


class Time(models.Model):
    Unit = [
        ("gal", "گالن"),
        ("but", "بوته",),
        ("kilo", "کیلو گرم")
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر',)
    shamsi_date = models.DateField(default=jdatetime.date.today, null=True, blank=True, verbose_name='تاریخ ')
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE, verbose_name='نوع عملیات', null=True, blank=True)
    volume = models.IntegerField(verbose_name='حجم مواد', null=True, blank=True)
    unit = models.CharField(choices=Unit, max_length=15, verbose_name='واحد محاسبه', null=True, blank=True)
    start_session = models.TimeField(max_length=20, verbose_name='از ساعت ', null=True, blank=True, default='08:00')
    end_session = models.TimeField(max_length=20, verbose_name='تا ساعت ', null=True, blank=True, default='12:00')

    def get_shamsi_date(self):
        # تبدیل تاریخ میلادی به شمسی برای نمایش
        print(f"self type: {type(self)}")
        return jdatetime.date.fromgregorian(date=self.shamsi_date).strftime("%Y/%m/%d")

    def __str__(self):
        return f"{self.user}{self.shamsi_date}{self.operation}"


