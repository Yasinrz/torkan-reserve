# Generated by Django 5.1.7 on 2025-06-12 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_alter_requestreservation_suggested_reservation_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='time',
            name='date_time_modified',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
