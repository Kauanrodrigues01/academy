# Generated by Django 5.1.3 on 2024-11-20 21:12

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_alter_member_start_date_alter_payment_payment_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='full_name',
            field=models.CharField(max_length=50, validators=[django.core.validators.MinLengthValidator(3)]),
        ),
    ]
