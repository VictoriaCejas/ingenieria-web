# Generated by Django 2.2.4 on 2019-09-03 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beautycalendar', '0003_auto_20190902_1851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='imagenAvatar',
            field=models.ImageField(blank=True, null=True, upload_to='avatar_image'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='imagenPortada',
            field=models.ImageField(blank=True, null=True, upload_to='front_image'),
        ),
    ]
