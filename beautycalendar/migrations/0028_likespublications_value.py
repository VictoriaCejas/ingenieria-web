# Generated by Django 2.2.4 on 2019-10-13 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beautycalendar', '0027_auto_20191011_2329'),
    ]

    operations = [
        migrations.AddField(
            model_name='likespublications',
            name='value',
            field=models.NullBooleanField(),
        ),
    ]
