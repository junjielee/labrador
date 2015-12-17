#!/usr/bin/env python
# encoding: utf-8

from django.contrib import admin

from .models import (
    Period,
    House,
    Tenant,
    Room,
    RoomRecord,
    Record,
)


class PeriodAdmin(admin.ModelAdmin):
    list_display = ['period']


class HouseAdmin(admin.ModelAdmin):
    list_display = ['name']


class TenantAdmin(admin.ModelAdmin):
    list_display = ['name', 'sex', 'phone']


class RoomAdmin(admin.ModelAdmin):
    list_display = ['number', 'status', 'rent', 'tenant']


class RecordAdmin(admin.ModelAdmin):
    list_display = ['room', 'total_fee']


class RoomRecordAdmin(admin.ModelAdmin):
    list_display = ['room', 'tenant', 'room_deposit', 'move_in_date']


admin.site.register(Period, PeriodAdmin)
admin.site.register(House, HouseAdmin)
admin.site.register(Tenant, TenantAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Record, RecordAdmin)
admin.site.register(RoomRecord, RoomRecordAdmin)
