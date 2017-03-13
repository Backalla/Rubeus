# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-13 12:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20170312_1638'),
    ]

    operations = [
        migrations.CreateModel(
            name='owner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('team_name', models.CharField(choices=[('SRH', 'Sunrisers Hyderabad'), ('RCB', 'Royal Challengers Bangalore'), ('RPS', 'Rising Pune Supergiants'), ('MIN', 'Mumbai Indians'), ('KKR', 'Kolkata Knight Riders'), ('KXP', 'Kings XI Punjab'), ('GJL', 'Gujarat Lions'), ('DDD', 'Delhi Daredevils')], default='SRH', max_length=3)),
                ('points', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]
