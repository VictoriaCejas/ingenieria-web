# Generated by Django 2.2.4 on 2019-09-09 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beautycalendar', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contentuser',
            name='description',
        ),
        migrations.AddField(
            model_name='contentuser',
            name='price',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
