# Generated by Django 5.1.3 on 2024-11-22 01:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0004_dailyreport_payments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activitylog',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 22, 1, 47, 42, 742997, tzinfo=datetime.timezone.utc), editable=False),
        ),
    ]
