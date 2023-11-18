# Generated by Django 4.2.3 on 2023-11-03 20:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=20)),
                ('date', models.DateField(default=datetime.date(2023, 11, 3))),
                ('content', models.CharField(max_length=5000)),
                ('story_id', models.IntegerField(default=1699045179.293074)),
            ],
        ),
    ]