# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-04 05:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('email', models.CharField(max_length=200)),
                ('message', models.TextField()),
                ('sent_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
