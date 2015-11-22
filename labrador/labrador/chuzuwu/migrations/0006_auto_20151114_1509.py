# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('chuzuwu', '0005_auto_20151114_1425'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timemodel',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 14, 15, 9, 32, 573634), verbose_name='Add time'),
        ),
        migrations.AlterField(
            model_name='timemodel',
            name='update_time',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 14, 15, 9, 32, 573723), verbose_name='Update time'),
        ),
    ]
