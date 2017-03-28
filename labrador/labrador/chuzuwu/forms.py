# -*- coding: utf-8 -*-

from django import forms
from .models import (
    Tenant,
    Room,
    RoomRecord,
    Record,
)


class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = ['name', 'sex', 'phone']


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['number', 'status', 'tenant', 'rent']


class RoomRecordForm(forms.ModelForm):
    class Meta:
        model = RoomRecord
        fields = ['room', 'period', 'tenant', 'rent', 'room_deposit', 'promise_deposit',
                  'tv_deposit', 'is_room_deposit_back', 'is_promise_deposit_back',
                  'is_tv_deposit_back', 'move_in_date', 'move_out_date', 'remark']


class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['room', 'period', 'rent_fee', 'electricity', 'electric_fee',
                  'internet_fee', 'charge_fee', 'tv_fee', 'special_fee', 'total_fee', 'remark']


# class UpdateRecordForm(forms.ModelForm):
#     class Meta:
#         model = Record
#         fields = ['room', 'period', 'electricity', 'watermeter', 'rent_fee',
#                   'electric_fee', 'water_fee', 'internet_fee', 'charge_fee',
#                   'total_fee', 'remark']
