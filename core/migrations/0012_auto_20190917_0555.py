# Generated by Django 2.2.5 on 2019-09-17 05:55

import datetime
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20190916_1328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='uploaded',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 9, 17, 5, 55, 53, 165328)),
        ),
        migrations.AlterField(
            model_name='chat',
            name='members',
            field=models.ManyToManyField(null=True, to=settings.AUTH_USER_MODEL, verbose_name='Member'),
        ),
        migrations.AlterField(
            model_name='chat',
            name='type',
            field=models.CharField(choices=[('DIALOG', 'Dialog'), ('CHAT', 'Chat')], default='DIALOG', max_length=30),
        ),
        migrations.AlterField(
            model_name='submission',
            name='Submitted_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 9, 17, 5, 55, 53, 165740)),
        ),
    ]