# Generated by Django 2.2.4 on 2019-10-07 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beautycalendar', '0022_auto_20191007_0534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdates',
            name='date',
            field=models.DateField(),
        ),
    ]