# Generated by Django 2.2.5 on 2019-09-17 07:22

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20190917_0700'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chat',
            name='user',
        ),
        migrations.AddField(
            model_name='chat',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='studentsss', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='chat',
            name='teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='teachersss', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='uploaded',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 9, 17, 7, 22, 41, 105636)),
        ),
        migrations.AlterField(
            model_name='submission',
            name='Submitted_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 9, 17, 7, 22, 41, 106056)),
        ),
    ]
