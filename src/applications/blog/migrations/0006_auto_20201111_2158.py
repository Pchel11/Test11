# Generated by Django 3.1.3 on 2020-11-11 18:58

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20201111_2157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 11, 18, 58, 44, 363993, tzinfo=utc)),
        ),
    ]
