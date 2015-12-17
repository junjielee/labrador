# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('chuzuwu', '0006_auto_20151114_1509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='period',
            name='period',
            field=models.DateField(default=datetime.date(2015, 11, 15), unique=True, verbose_name='Record period'),
        ),
        migrations.AlterField(
            model_name='room',
            name='status',
            field=models.CharField(default=b'L', max_length=1, verbose_name='Room status', choices=[(b'L', 'Lived'), (b'E', 'Empty')]),
        ),
        migrations.AlterField(
            model_name='timemodel',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 15, 0, 3, 10, 695358), verbose_name='Add time'),
        ),
        migrations.AlterField(
            model_name='timemodel',
            name='update_time',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 15, 0, 3, 10, 695443), verbose_name='Update time'),
        ),
    ]
