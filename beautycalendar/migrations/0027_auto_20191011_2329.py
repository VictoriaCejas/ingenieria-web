# Generated by Django 2.2.4 on 2019-10-11 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beautycalendar', '0026_reports'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reports',
            name='informed',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='reports',
            name='informer',
            field=models.EmailField(max_length=254),
        ),
    ]
