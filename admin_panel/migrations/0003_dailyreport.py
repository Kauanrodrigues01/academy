# Generated by Django 5.1.3 on 2024-11-19 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0002_alter_activitylog_member'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(unique=True)),
                ('active_students', models.PositiveIntegerField(default=0)),
                ('pending_students', models.PositiveIntegerField(default=0)),
                ('new_students', models.PositiveIntegerField(default=0)),
                ('daily_profit', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
            ],
            options={
                'indexes': [models.Index(fields=['date'], name='admin_panel_date_1ce761_idx')],
            },
        ),
    ]