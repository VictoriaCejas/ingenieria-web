# Generated by Django 2.2.4 on 2019-09-04 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('state', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'active'), (2, 'pending activation'), (3, 'locked'), (4, 'removed')], null=True)),
                ('kind', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'bussines'), (2, 'client'), (3, 'administrator')], null=True)),
                ('score', models.PositiveSmallIntegerField(null=True)),
                ('imageAvatar', models.ImageField(blank=True, null=True, upload_to='avatar_image')),
                ('imageFront', models.ImageField(blank=True, null=True, upload_to='front_image')),
                ('description', models.CharField(blank=True, max_length=250, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
