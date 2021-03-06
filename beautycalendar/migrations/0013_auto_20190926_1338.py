# Generated by Django 2.2.4 on 2019-09-26 13:38

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('beautycalendar', '0012_auto_20190926_1334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contentusers',
            name='imageProduct',
            field=django_resized.forms.ResizedImageField(blank=True, crop=['middle', 'center'], force_format='JPEG', keep_meta=True, null=True, quality=90, size=[100, 100], upload_to='Products'),
        ),
        migrations.AlterField(
            model_name='empleoyees',
            name='imageEmpleoyee',
            field=django_resized.forms.ResizedImageField(blank=True, crop=['middle', 'center'], force_format='JPEG', keep_meta=True, null=True, quality=90, size=[100, 100], upload_to='Employees'),
        ),
        migrations.AlterField(
            model_name='users',
            name='imageFront',
            field=django_resized.forms.ResizedImageField(blank=True, crop=['middle', 'center'], force_format='JPEG', keep_meta=True, null=True, quality=90, size=[1281, 236], upload_to='front_image'),
        ),
    ]
