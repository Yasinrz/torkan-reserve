# Generated by Django 5.1.7 on 2025-05-01 09:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_remove_time_user_time_date_time_reserved_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestreservation',
            name='suggested_reservation_date',
            field=models.DateField(blank=True, default=datetime.date.today, null=True, verbose_name='reservation date'),
        ),
    ]
