# Generated by Django 2.2.4 on 2019-09-25 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beautycalendar', '0007_auto_20190917_2330'),
    ]

    operations = [
        migrations.AddField(
            model_name='beautysalons',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]