# Generated by Django 2.2.7 on 2020-04-06 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20200406_1337'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usermodel',
            name='password1',
        ),
        migrations.RemoveField(
            model_name='usermodel',
            name='password2',
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='vk',
            field=models.CharField(blank=True, default='narEz', max_length=200, null=True),
        ),
    ]
