# Generated by Django 4.2.3 on 2023-11-06 19:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_story_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='date',
            field=models.DateField(null=True, verbose_name=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='story',
            name='state',
            field=models.CharField(blank=True, choices=[('Draft', 'Draft'), ('Awaiting Editor Approval', 'Awaiting Editor Approval'), ('Awaiting Supervisor Approval', 'Awaiting Supervisor Approval'), ('Published', 'Published'), ('Deleted', 'Deleted')], default='Draft', max_length=30, null=True),
        ),
    ]
