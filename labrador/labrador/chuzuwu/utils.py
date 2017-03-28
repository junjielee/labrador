# -*- coding: utf-8 -*-

from .models import (
    Record,
    Period,
    RoomRecord,
)
from ..settings import (
    INTERNET_FEE,
    CHARGE_FEE,
    TV_FEE,
)


def get_first_no_record_room(all_rooms, all_periods):
    """获取第一个没有入住记录的房

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
    """获取上一个记录时期

    :return: 上一个period, 找不到则返回None
    :type return: Period
    """

    cur_month = period.period.month
    last_year = period.period.year
    last_month = cur_month - 1
    if last_month == 0:
        last_year -= 1
        last_month = 12

    try:
        last_period = Period.objects.get(period__year=last_year,
                                         period__month=last_month)
    except Period.DoesNotExist:
        last_period = None
    return last_period


def get_next_period(period):
    """获取下一个记录时期

    :return: 下一个period, 找不到则返回None
    :type return: Period
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
    """计算电费"""

    # TODO加上判断这个月份的电度数是否少于上月分
    electric_fee = (cur_electricity - last_electricity) * per_fee

    return electric_fee


def calculate_water_fee(cur_water, last_water, per_fee):
    """计算水费"""

    # TODO加上判断这个月份的水度数是否少于上月分
    water_fee = (cur_water - last_water) * per_fee

    return water_fee


def calculate_total_fee(datas):
    """计算total_fee的值"""

    total_fee = (
        int(datas.get('rent_fee', 0)) +
        float(datas.get('electric_fee', 0)) +
        int(datas.get('charge_fee', 0)) +
        int(datas.get('internet_fee', 0)) +
        int(datas.get('tv_fee', 0)) +
        int(datas.get('special_fee', 0))
    )
    return total_fee


# def set_room_info(room, datas):
#     """设置room的状态，信息等"""

#     return None


def get_room_tenant(room):
    """获取当前房间的租客

    :type return: Tenant
    """

    if room.status == 'E':
        return None

    room_records = RoomRecord.objects.filter(room=room).order_by('-period')
    if room_records.count() > 0:
        return room_records[0].tenant
    else:
        return None


def file_iterator(file_name, chunk_size=512):
    """用于下载文件,适应下载大小文件"""

    with open(file_name) as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break


def handle_upload_record_file(file, path):
    """处理上传文件"""

    new_file = path + file.name
    with open(new_file, 'wb+') as f:
        for chunk in file.chunks():
            f.write(chunk)


def get_monthly_statistics(records):
    """获取每月统计信息"""

    record_count = {
        'number': u'合计',
        'rent': 0,
        'electric': 0,
        'internet': 0,
        'charge': 0,
        'tv': 0,
        'special': 0,
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
        record_count['special'] += record.special_fee
        record_count['total'] += record.total_fee
        if not record.is_get_money:
            record_count['num_no_money'] += 1

    record_count['remark'] = u'没给钱的有%s个' % record_count['num_no_money']
    return record_count


def get_record_type(datas):
    """判断record类型：入住的收入，退房的收入，还是稳定每月的收入

    :param datas: 请求表单中的数据
    :type datas: QueryDict
    :return: 字符串move_in, move_out, or monthly
    """
    if datas.get('electric_fee') == 0 and datas.get('rent_fee') != 0:
        return 'move_in'
    elif datas.get('electric_fee') != 0 and datas.get('rent_fee') != 0:
        return 'monthly'
    else:
        return 'move_out'


def change_form_fee(datas):
    """改变form.POST中的网费，充电费，电视费，输入的是有还是没

    :param datas: 请求表单中的数据
    :type datas: QueryDict
    :return: 修改为费用值的datas
    """
    if datas.get('internet_fee'):
        datas.setlist('internet_fee', [unicode(INTERNET_FEE)])
    else:
        datas.setlist('internet_fee', [unicode(0)])
    if datas.get('charge_fee'):
        datas.setlist('charge_fee', [unicode(CHARGE_FEE)])
    else:
        datas.setlist('charge_fee', [unicode(0)])
    if datas.get('tv_fee'):
        datas.setlist('tv_fee', [unicode(TV_FEE)])
    else:
        datas.setlist('tv_fee', [unicode(0)])
    return datas
