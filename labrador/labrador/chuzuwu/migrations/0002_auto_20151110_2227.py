# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('chuzuwu', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='special_fee',
            field=models.IntegerField(default=0, verbose_name='Specail fee'),
        ),
        migrations.AlterField(
            model_name='timemodel',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 10, 22, 27, 50, 781798), verbose_name='Add time'),
        ),
        migrations.AlterField(
            model_name='timemodel',
            name='update_time',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 10, 22, 27, 50, 781938), verbose_name='Update time'),
        ),
    ]
