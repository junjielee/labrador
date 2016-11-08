#!/usr/bin/env python
# encoding: utf-8

from datetime import datetime, date
from django.db import models
from django.utils.translation import ugettext_lazy as _


ROOM_STATUS=(
    ('L', _('Lived')),
    ('E', _('Empty'))
)
GENDER_CHOICES = (
    ('M', _('Male')),
    ('F', _('Female')),
)


class TimeModel(models.Model):
    add_time = models.DateTimeField(default=datetime.now(),
                                    verbose_name=_('Add time'))
    update_time = models.DateTimeField(default=datetime.now(),
                                       verbose_name=_('Update time'))


class Period(models.Model):
    period = models.DateField(default=date.today(),
                              unique=True,
                              verbose_name=_('Record period'))

    def __unicode__(self):
        return u'%s年%s月' % (self.period.year, self.period.month)

    class Meta:
        verbose_name = _('Record period')
        verbose_name_plural = _('Record periods')


class House(models.Model):
    name = models.CharField(max_length=100,
                            verbose_name=_('House name'),
                            unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('House')
        verbose_name_plural = _('Houses')


class Tenant(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Tenant name'))
    sex = models.CharField(max_length=1,
                           blank=True,
                           choices=GENDER_CHOICES,
                           verbose_name=_('Tenant sex'))
    phone = models.CharField(max_length=20,
                             blank=True,
                             verbose_name=_('Tenant phone'))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('Tenant')
        verbose_name_plural = _('Tenants')


class Room(models.Model):
    number = models.IntegerField(unique=True, verbose_name=_('Room number'))
    house = models.ForeignKey(House, verbose_name=_('House'))
    status = models.CharField(max_length=1,
                              default=ROOM_STATUS[0][0],
                              choices=ROOM_STATUS,
                              verbose_name=_('Room status'))
    tenant = models.ForeignKey(Tenant, blank=True, null=True, verbose_name=_('Tenant'))
    rent = models.IntegerField(blank=True, null=True, verbose_name=_('Room rent'))

    def __unicode__(self):
        return u'%s-%s' % (self.house, self.number)

    class Meta:
        verbose_name = _('Room')
        verbose_name_plural = _('Rooms')


class RoomRecord(TimeModel):
    room = models.ForeignKey(Room, verbose_name=_('Room'))
    period = models.ForeignKey(Period, verbose_name=_('Period'))
    tenant = models.ForeignKey(Tenant, blank=True, null=True, verbose_name=_('Tenant'))
    rent = models.IntegerField(blank=True, null=True, verbose_name=_('Room rent'))
    room_deposit = models.IntegerField(verbose_name=_('Room deposit'))
    promise_deposit = models.IntegerField(verbose_name=_('Promise deposit'))
    tv_deposit = models.IntegerField(verbose_name=_('TV deposit'))
    is_room_deposit_back = models.BooleanField(default=False,
                                               verbose_name=_('Is room deposit back'))
    is_promise_deposit_back = models.BooleanField(default=False,
                                                  verbose_name=_('Is promise deposit back'))
    is_tv_deposit_back = models.BooleanField(default=False,
                                             verbose_name=_('Is tv deposit back'))
    move_in_date = models.DateField(verbose_name=_('Move in date'))
    move_out_date = models.DateField(blank=True, null=True,
                                     verbose_name=_('Move out date'))
    remark = models.CharField(blank=True,
                              max_length=512,
                              verbose_name=_('RoomRecord remark'))

    def __unicode__(self):
        return u'%s-%s' % (self.room, self.tenant)

    def is_finish(self):
        return self.is_room_deposit_back and self.is_promise_deposit_back and self.is_tv_deposit_back

    class Meta:
        verbose_name = _('RoomRecord')
        verbose_name_plural = _('RoomRecords')


class Record(TimeModel):
    room = models.ForeignKey(Room, verbose_name=_('Room'))
    period = models.ForeignKey(Period, verbose_name=_('Period'))
    tenant = models.ForeignKey(Tenant, blank=True, null=True, verbose_name=_('Tenant'))
    electricity = models.FloatField(default=0,
                                    verbose_name=_('Quantity of electricity'))
    watermeter = models.FloatField(default=0,
                                   verbose_name=_('Quantity of water'))
    electric_fee = models.FloatField(default=0,
                                     verbose_name=_('Electirc fee'))
    water_fee = models.FloatField(default=0,
                                  verbose_name=_('Water fee'))
    rent_fee = models.IntegerField(default=0,
                                   verbose_name=_('Rent fee'))
    internet_fee = models.IntegerField(default=0,
                                       verbose_name=_('Internet fee'))
    charge_fee = models.IntegerField(default=0,
                                     verbose_name=_('Charge fee'))
    tv_fee = models.IntegerField(default=0,
                                 verbose_name=_('TV fee'))
    special_fee = models.IntegerField(default=0,
                                      verbose_name=_('Specail fee'))
    total_fee = models.FloatField(default=0,
                                  verbose_name=_('Total fee'))
    is_get_money = models.BooleanField(default=True,
                                       verbose_name=_('Is get money'))
    remark = models.CharField(blank=True,
                              max_length=512,
                              verbose_name=_('Record remark'))

    def __unicode__(self):
        return u'%s-￥%s' % (self.room, self.total_fee)

    class Meta:
        unique_together = ("room", "period", "tenant")
        verbose_name = _('Record')
        verbose_name_plural = _('Records')
