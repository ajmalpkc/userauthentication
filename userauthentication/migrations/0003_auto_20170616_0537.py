# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-16 05:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauthentication', '0002_remove_userprofile_uemail'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='uname',
            field=models.CharField(default='username', max_length=200),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='uphone',
            field=models.CharField(default='9999999999', max_length=100),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='uvechicle',
            field=models.CharField(default='KL', max_length=200),
        ),
    ]
