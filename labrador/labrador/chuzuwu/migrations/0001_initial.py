# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='House',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100, verbose_name='House name')),
            ],
            options={
                'verbose_name': 'House',
                'verbose_name_plural': 'Houses',
            },
        ),
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('period', models.DateField(default=datetime.date(2015, 11, 10), unique=True, verbose_name='Record period')),
            ],
            options={
                'verbose_name': 'Record period',
                'verbose_name_plural': 'Record periods',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField(unique=True, verbose_name='Room number')),
                ('status', models.CharField(max_length=1, verbose_name='Room status', choices=[(b'L', 'Lived'), (b'E', 'Empty')])),
                ('rent', models.IntegerField(null=True, verbose_name='Room rent', blank=True)),
                ('house', models.ForeignKey(verbose_name='House', to='chuzuwu.House')),
            ],
            options={
                'verbose_name': 'Room',
                'verbose_name_plural': 'Rooms',
            },
        ),
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='Tenant name')),
                ('sex', models.CharField(blank=True, max_length=1, verbose_name='Tenant sex', choices=[(b'M', b'Male'), (b'F', b'Female')])),
                ('phone', models.CharField(max_length=20, verbose_name='Tenant phone', blank=True)),
            ],
            options={
                'verbose_name': 'Tenant',
                'verbose_name_plural': 'Tenants',
            },
        ),
        migrations.CreateModel(
            name='TimeModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('add_time', models.DateTimeField(default=datetime.datetime(2015, 11, 10, 0, 58, 55, 538450), verbose_name='Add time')),
                ('update_time', models.DateTimeField(default=datetime.datetime(2015, 11, 10, 0, 58, 55, 538526), verbose_name='Update time')),
            ],
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('timemodel_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='chuzuwu.TimeModel')),
                ('electricity', models.FloatField(default=0, verbose_name='Quantity of electricity')),
                ('watermeter', models.FloatField(default=0, verbose_name='Quantity of water')),
                ('electric_fee', models.FloatField(default=0, verbose_name='Electirc fee')),
                ('water_fee', models.FloatField(default=0, verbose_name='Water fee')),
                ('rent_fee', models.IntegerField(default=0, verbose_name='Rent fee')),
                ('internet_fee', models.IntegerField(default=0, verbose_name='Internet fee')),
                ('charge_fee', models.IntegerField(default=0, verbose_name='Charge fee')),
                ('tv_fee', models.IntegerField(default=0, verbose_name='TV fee')),
                ('total_fee', models.FloatField(default=0, verbose_name='Total fee')),
                ('is_get_money', models.BooleanField(default=True, verbose_name='Is get money')),
                ('remark', models.CharField(max_length=512, verbose_name='Record remark', blank=True)),
                ('period', models.ForeignKey(verbose_name='Period', to='chuzuwu.Period')),
            ],
            options={
                'verbose_name': 'Record',
                'verbose_name_plural': 'Records',
            },
            bases=('chuzuwu.timemodel',),
        ),
        migrations.CreateModel(
            name='RoomRecord',
            fields=[
                ('timemodel_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='chuzuwu.TimeModel')),
                ('rent', models.IntegerField(null=True, verbose_name='Room rent', blank=True)),
                ('room_deposit', models.IntegerField(verbose_name='Room deposit')),
                ('promise_deposit', models.IntegerField(verbose_name='Promise deposit')),
                ('tv_deposit', models.IntegerField(verbose_name='TV deposit')),
                ('is_room_deposit_back', models.BooleanField(default=False, verbose_name='Is room deposit back')),
                ('is_promise_deposit_back', models.BooleanField(default=False, verbose_name='Is promise deposit back')),
                ('is_tv_deposit_back', models.BooleanField(default=False, verbose_name='Is tv deposit back')),
                ('move_in_date', models.DateTimeField(verbose_name='Move in date')),
                ('move_out_date', models.DateTimeField(null=True, verbose_name='Move out date', blank=True)),
                ('remark', models.CharField(max_length=512, verbose_name='RoomRecord remark', blank=True)),
                ('period', models.ForeignKey(verbose_name='Period', to='chuzuwu.Period')),
            ],
            options={
                'verbose_name': 'RoomRecord',
                'verbose_name_plural': 'RoomRecords',
            },
            bases=('chuzuwu.timemodel',),
        ),
        migrations.AddField(
            model_name='room',
            name='tenant',
            field=models.ForeignKey(verbose_name='Tenant', blank=True, to='chuzuwu.Tenant', null=True),
        ),
        migrations.AddField(
            model_name='roomrecord',
            name='room',
            field=models.ForeignKey(verbose_name='Room', to='chuzuwu.Room'),
        ),
        migrations.AddField(
            model_name='roomrecord',
            name='tenant',
            field=models.ForeignKey(verbose_name='Tenant', blank=True, to='chuzuwu.Tenant', null=True),
        ),
        migrations.AddField(
            model_name='record',
            name='room',
            field=models.ForeignKey(verbose_name='Room', to='chuzuwu.Room'),
        ),
        migrations.AddField(
            model_name='record',
            name='tenant',
            field=models.ForeignKey(verbose_name='Tenant', blank=True, to='chuzuwu.Tenant', null=True),
        ),
    ]
