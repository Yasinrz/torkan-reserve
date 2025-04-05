# Generated by Django 5.1.7 on 2025-04-05 11:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_user_phone_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='time',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='time',
            name='username',
        ),
        migrations.AddField(
            model_name='time',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='home.user', verbose_name='کاربر'),
            preserve_default=False,
        ),
    ]
