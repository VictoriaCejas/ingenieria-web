# Generated by Django 2.2.4 on 2019-09-10 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beautycalendar', '0003_auto_20190910_0418'),
    ]

    operations = [
        migrations.AddField(
            model_name='publications',
            name='state',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'active'), (3, 'pending activation'), (4, 'removed')], null=True),
        ),
    ]