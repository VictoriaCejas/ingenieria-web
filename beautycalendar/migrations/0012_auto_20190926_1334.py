# Generated by Django 2.2.4 on 2019-09-26 13:34

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('beautycalendar', '0011_auto_20190926_1324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='imageFront',
            field=django_resized.forms.ResizedImageField(blank=True, crop=['middle', 'center'], force_format='JPEG', keep_meta=True, null=True, quality=90, size=[1281, 235.19], upload_to='front_image'),
        ),
    ]
