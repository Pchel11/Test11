# Generated by Django 3.1.3 on 2020-11-18 12:45

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('content', models.CharField(blank=True, max_length=5000, null=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2020, 11, 18, 12, 45, 29, 251951, tzinfo=utc))),
                ('visible', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['-created_at', 'title', 'pk'],
            },
        ),
    ]