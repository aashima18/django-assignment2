# Generated by Django 2.2.5 on 2019-09-12 13:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20190912_1339'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignment',
            name='requestt',
        ),
        migrations.AlterField(
            model_name='assignment',
            name='uploaded',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 9, 12, 13, 40, 21, 867252)),
        ),
        migrations.AlterField(
            model_name='submission',
            name='Submitted_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 9, 12, 13, 40, 21, 867672)),
        ),
    ]