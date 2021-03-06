# Generated by Django 2.2.5 on 2019-09-16 13:28

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20190916_1159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='uploaded',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 9, 16, 13, 28, 17, 130608)),
        ),
        migrations.AlterField(
            model_name='message',
            name='chat',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Chat', verbose_name='Chat'),
        ),
        migrations.AlterField(
            model_name='submission',
            name='Submitted_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 9, 16, 13, 28, 17, 131119)),
        ),
    ]
