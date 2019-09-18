# Generated by Django 2.2.5 on 2019-09-17 07:00

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20190917_0658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='uploaded',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 9, 17, 7, 0, 7, 860366)),
        ),
        migrations.AlterField(
            model_name='submission',
            name='Submitted_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 9, 17, 7, 0, 7, 860797)),
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('message', models.CharField(max_length=300)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]