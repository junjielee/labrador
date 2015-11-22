# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('chuzuwu', '0002_auto_20151110_2227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomrecord',
            name='move_in_date',
            field=models.DateField(verbose_name='Move in date'),
        ),
        migrations.AlterField(
            model_name='roomrecord',
            name='move_out_date',
            field=models.DateField(null=True, verbose_name='Move out date', blank=True),
        ),
        migrations.AlterField(
            model_name='timemodel',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 10, 23, 33, 8, 642179), verbose_name='Add time'),
        ),
        migrations.AlterField(
            model_name='timemodel',
            name='update_time',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 10, 23, 33, 8, 642248), verbose_name='Update time'),
        ),
    ]
