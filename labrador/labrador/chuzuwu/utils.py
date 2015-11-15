#!/usr/bin/env python
# encoding: utf-8

from .models import (
    Record,
    Period,
    RoomRecord,
)


def get_first_no_record_room(all_rooms, all_periods):
    """
        默认去最近的日期的一个为当前日期, 返回当前还没输入记录的room，
        如果都输入了，就返回number第一个的room
    """
    cur_period = all_periods[0]
    cur_room = all_rooms[0]
    cur_period_records = Record.objects.filter(period=cur_period)\
        .select_related('room').order_by('room__number')
    for room in all_rooms:
        if not filter(lambda x: x.room == room, cur_period_records):
            cur_room = room
            break
    return cur_room


def get_last_period(period):
    """
        获取上一个记录时期
    """
    cur_month = period.period.month
    last_year = period.period.year
    last_month = cur_month - 1
    if last_month == 0:
        last_year -= 1
        last_month = 12
    # 先简单处理错误,找不到返回None
    try:
        last_period = Period.objects.get(period__year=last_year,
                                         period__month=last_month)
    except Period.DoesNotExist:
        last_period = None
    return last_period


def get_next_period(period):
    """
        获取下一个记录时期
    """
    cur_month = period.period.month
    next_year = period.period.year
    next_month = cur_month + 1
    if next_month >= 13:
        next_year += 1
        next_month = 1
    try:
        next_period = Period.objects.get(period__year=next_year,
                                         period__month=next_month)
    except Period.DoesNotExist:
        next_period = None
    return next_period


def calculate_electric_fee(cur_electricity, last_electricity, per_fee):
    # 加上判断这个月份的电度数是否少于上月分
    electric_fee = (cur_electricity - last_electricity) * per_fee

    return electric_fee


def calculate_water_fee(cur_water, last_water, per_fee):
    # 加上判断这个月份的水度数是否少于上月分
    water_fee = (cur_water - last_water) * per_fee

    return water_fee


def calculate_total_fee(datas):
    """
        计算total_fee的值
    """
    total_fee = (
        int(datas.get('rent_fee')) +
        float(datas.get('electric_fee')) +
        int(datas.get('charge_fee')) +
        int(datas.get('internet_fee')) +
        int(datas.get('tv_fee'))
    )
    print total_fee
    return total_fee


def set_room_info(room, datas):
    """
        设置room的状态，信息等
    """
    return None


def get_room_tenant(room):
    """
        获取当前房间的租客,返回tenant对象
    """
    if room.status == 'E':
        return None
    room_records = RoomRecord.objects.filter(room=room).order_by('-period')
    if room_records.count() > 0:
        return room_records[0].tenant
    else:
        return None


# 用于下载文件,适应下载大小文件
def file_iterator(file_name, chunk_size=512):
    with open(file_name) as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break


# 处理上传文件
def handle_upload_record_file(file, path):
    new_file = path + file.name
    with open(new_file, 'wb+') as f:
        for chunk in file.chunks():
            f.write(chunk)


# 添加统计信息
def get_monthly_statistics(records):
    record_count = {
        'number': u'合计',
        'rent': 0,
        'electric': 0,
        'internet': 0,
        'charge': 0,
        'tv': 0,
        'total': 0,
        'num_no_money': 0,
    }
    # 统计
    for record in records:
        record_count['rent'] += record.rent_fee
        record_count['electric'] += record.electric_fee
        record_count['internet'] += record.internet_fee
        record_count['charge'] += record.charge_fee
        record_count['tv'] += record.tv_fee
        record_count['total'] += record.total_fee
        if not record.is_get_money:
            record_count['num_no_money'] += 1
    record_count['remark'] = u'没给钱的有%s个' % record_count['num_no_money']
    return record_count
