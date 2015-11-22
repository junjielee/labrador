# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('chuzuwu', '0004_auto_20151111_0038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='period',
            name='period',
            field=models.DateField(default=datetime.date(2015, 11, 14), unique=True, verbose_name='Record period'),
        ),
        migrations.AlterField(
            model_name='timemodel',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 14, 14, 25, 2, 910901), verbose_name='Add time'),
        ),
        migrations.AlterField(
            model_name='timemodel',
            name='update_time',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 14, 14, 25, 2, 910971), verbose_name='Update time'),
        ),
    ]
