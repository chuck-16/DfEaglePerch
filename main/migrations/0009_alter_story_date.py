# Generated by Django 4.2.3 on 2023-11-06 02:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_story_state_alter_story_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='date',
            field=models.DateField(verbose_name=django.utils.timezone.now),
        ),
    ]
