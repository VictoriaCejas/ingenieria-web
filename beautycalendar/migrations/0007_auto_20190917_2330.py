# Generated by Django 2.2.4 on 2019-09-17 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beautycalendar', '0006_auto_20190917_2310'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdates',
            name='state',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'confirmed'), (2, 'cancel'), (3, 'finalized')], null=True),
        ),
        migrations.AlterField(
            model_name='publications',
            name='state',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'active'), (2, 'locked'), (3, 'removed')], null=True),
        ),
    ]
