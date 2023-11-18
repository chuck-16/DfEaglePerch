# Generated by Django 4.2.3 on 2023-11-05 00:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import main.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='category',
            field=models.CharField(choices=[('Opinion', 'Opinion'), ('Sports', 'Sports'), ('School', 'School'), ('Current Events', 'Current Events')], default='School', max_length=20),
        ),
        migrations.AlterField(
            model_name='story',
            name='author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='story',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='story',
            name='story_id',
            field=models.CharField(default=main.models.generate_unique_id, editable=False, max_length=4, unique=True),
        ),
        migrations.CreateModel(
            name='ReadingList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reading_list', models.CharField(default='[]', max_length=1000)),
                ('assigned_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]