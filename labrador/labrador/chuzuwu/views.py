#!/usr/bin/env python
# encoding: utf-8

import xlrd
import xlwt
import json
from datetime import date as module_date

from django.shortcuts import (
    render,
    render_to_response,
    RequestContext,
    redirect,
)
from django.contrib.auth.decorators import login_required
from django.http import StreamingHttpResponse, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.conf import settings
from ..settings import (
    EXCEL_RECORD_COL,
    EXCEL_PATH,
    RETURN_MSG,
)

from .models import (
    Period,
    Record,
    Tenant,
    Room,
    House,
    RoomRecord,
    GENDER_CHOICES,
    ROOM_STATUS,
)
from .forms import (
    TenantForm,
    RoomForm,
    RecordForm,
    RoomRecordForm,
)
from .utils import (
    get_first_no_record_room,
    get_last_period,
    get_next_period,
    get_room_tenant,
    calculate_total_fee,
    file_iterator,
    handle_upload_record_file,
    get_monthly_statistics,
    change_form_fee,
)


@login_required
def index(request):
    return render(request, 'chuzuwu/index.html')


@login_required
def money_index(request):
    # 取最近的一个记录日期
    period_id = int(request.GET.get('period_id', '0'))
    if request.method == 'POST':
        date_str = request.POST.get('search_date')
        year = int(date_str.split('-')[0])
        month = int(date_str.split('-')[1])
        cur_date = module_date(year, month, 1)
        try:
            period = Period.objects.get(period=cur_date)
        except Period.DoesNotExist:
            period_id = 0
        else:
            period_id = period.id

    if period_id == 0:
        try:
            period = Period.objects.order_by('-period').first()
        except Period.DoesNotExist:
            period = None
        if period is not None:
            previous_period = get_last_period(period)
            next_period = get_next_period(period)
        else:
            previous_period = None
            next_period = None
    else:
        period = Period.objects.get(id=period_id)
        previous_period = get_last_period(period)
        next_period = get_next_period(period)
    records = Record.objects.filter(period=period).order_by('room__number')\
        .select_related('room', 'period')
    record_count = get_monthly_statistics(records)
    context = RequestContext(request, {
        'records': records,
        'record_count': record_count,
        'cur_period': period,
        'previous_period': previous_period,
        'next_period': next_period,
    })
    return render_to_response('chuzuwu/money-index.html',
                              context_instance=context)


@login_required
def money_add(request):
    period_options = Period.objects.all().order_by('-period')
    room_options = Room.objects.all().order_by('number')
    if request.method == 'POST':
        datas = request.POST.copy()
        room_id = datas.get('room')
        if room_id != '':
            room = Room.objects.get(id=int(room_id))
        tenant = get_room_tenant(room)
        if tenant is None:
            messages.info(request, '%s房间还没入住记录,请先添加入住记录' % room.number)
            return redirect('room_record_add')
        datas.setlist('tenant', [unicode(tenant.id)])
        datas.setlist('rent_fee', [unicode(room.rent)])
        datas = change_form_fee(datas)
        period_id = datas.get('period')
        if tenant:
            try:
                record = Record.objects.get(room_id=int(room_id),
                                            period_id=int(period_id),
                                            tenant=tenant)
            except Record.DoesNotExist:
                total_fee = calculate_total_fee(datas)
                datas.setlist('total_fee', [unicode(total_fee)])
                form = RecordForm(datas)
                if form.is_valid():
                    form.save()
            else:
                messages.info(request, '%s入住的房间%s，这个月已经有记录了' %
                    (tenant.name, room.number))
            finally:
                cur_period_records = Record.objects.filter(period_id=period_id)\
                    .select_related('room').order_by('room__number')
                if cur_period_records.count() == room_options.count():
                    return redirect(reverse('money'))
                else:
                    return redirect(reverse('money_add'))
        return redirect(reverse('money'))

    record_form = RecordForm()
    # 获取当前周期还没输入的一个room
    cur_room = get_first_no_record_room(room_options, period_options)

    context = RequestContext(request, {
        'record_form': record_form,
        'period_options': period_options,
        'room_options': room_options,
        'cur_room': cur_room,
    })
    return render_to_response('chuzuwu/money-add.html',
                              context_instance=context)


@login_required
def money_update(request, rid):
    try:
        record = Record.objects.get(id=rid)
    except Record.DoesNotExist:
        print 'money update error, record not found'
    if request.method == 'POST':
        datas = request.POST.copy()
        datas = change_form_fee(datas)

        total_fee = calculate_total_fee(datas)
        datas.setlist('total_fee', [unicode(total_fee)])
        form = RecordForm(datas, instance=record)
        if form.is_valid():
            form.save()
        else:
            messages.error(request, '更新失败，请检查输入')
        return redirect(reverse('money'))

    record_form = RecordForm()
    period_options = Period.objects.all().order_by('-period')
    tenant_options = Tenant.objects.all()
    context = RequestContext(request, {
        'record': record,
        'record_form': record_form,
        'period_options': period_options,
        'tenant_options': tenant_options,
    })
    return render_to_response('chuzuwu/money-update.html',
                              context_instance=context)


@login_required
def tenant_index(request):
    tenants = Tenant.objects.all()
    context = RequestContext(request, {
        'tenants': tenants,
    })
    return render_to_response('chuzuwu/tenant-index.html',
                              context_instance=context)


@login_required
def tenant_add(request):
    if request.method == 'POST':
        form = TenantForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            messages.error(request, '租客添加失败')
        return redirect(reverse('tenant'))
    sex_options = list()
    for sex in GENDER_CHOICES:
        sex_options.append({
            'value': sex[0],
            'full_value': sex[1]
        })
    tenant_form = TenantForm()
    context = RequestContext(request, {
        'tenant_form': tenant_form,
        'sex_options': sex_options,
    })
    return render_to_response('chuzuwu/tenant-add.html',
                              context_instance=context)


@login_required
def tenant_update(request, tid):
    try:
        tenant = Tenant.objects.get(id=tid)
    except Tenant.DoesNotExist:
        print 'tenant not found'
    if request.method == 'POST':
        datas = request.POST
        form = TenantForm(datas, instance=tenant)
        if form.is_valid():
            form.save()
        else:
            messages.error(request, '租客修改信息失败')
        return redirect(reverse('tenant'))

    tenant_form = TenantForm()
    sex_options = list()
    for sex in GENDER_CHOICES:
        sex_options.append({
            'value': sex[0],
            'full_value': sex[1]
        })
    context = RequestContext(request, {
        'tenant_form': tenant_form,
        'tenant': tenant,
        'sex_options': sex_options,
    })
    return render_to_response('chuzuwu/tenant-update.html',
                              context_instance=context)


@login_required
def room_index(request):
    rooms = Room.objects.all().order_by('number')
    context = RequestContext(request, {
        'rooms': rooms,
    })
    return render_to_response('chuzuwu/room-index.html',
                              context_instance=context)


@login_required
def room_add(request):
    if request.method == 'POST':
        house = House.objects.first()
        room = Room(house=house)
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
        else:
            messages.error(request, '房间添加失败')
        return redirect(reverse('room'))

    status_options = list()
    for status in ROOM_STATUS:
        status_options.append({
            'value': status[0],
            'full_value': status[1]
        })
    tenant_options = Tenant.objects.all()
    room_form = RoomForm()
    context = RequestContext(request, {
        'room_form': room_form,
        'status_options': status_options,
        'tenant_options': tenant_options,
    })
    return render_to_response('chuzuwu/room-add.html',
                              context_instance=context)


@login_required
def room_update(request, rid):
    try:
        room = Room.objects.get(id=rid)
    except Room.DoesNotExist:
        print 'room update error, room not found'
    if request.method == 'POST':
        datas = request.POST
        form = RoomForm(datas, instance=room)
        print form
        if form.is_valid():
            form.save()
        else:
            messages.error(request, '房间更新不成功,请检查输入')
        return redirect(reverse('room'))

    status_options = list()
    for status in ROOM_STATUS:
        status_options.append({
            'value': status[0],
            'full_value': status[1]
        })
    tenant_options = Tenant.objects.all()
    room_form = RoomForm()
    context = RequestContext(request, {
        'room': room,
        'room_form': room_form,
        'status_options': status_options,
        'tenant_options': tenant_options,
    })
    return render_to_response('chuzuwu/room-update.html',
                              context_instance=context)


@login_required
def room_record(request):
    # 取最近的一个记录日期
    period_id = int(request.GET.get('period_id', '0'))
    if period_id == 0:
        try:
            period = Period.objects.order_by('-period').first()
        except Period.DoesNotExist:
            period = None
        if period is not None:
            previous_period = get_last_period(period)
            next_period = get_next_period(period)
        else:
            previous_period = None
            next_period = None
    else:
        period = Period.objects.get(id=period_id)
        previous_period = get_last_period(period)
        next_period = get_next_period(period)
    room_records = RoomRecord.objects.filter(period=period)\
        .order_by('-period', 'room__number').select_related('room', 'period')
    context = RequestContext(request, {
        'room_records': room_records,
        'cur_period': period,
        'previous_period': previous_period,
        'next_period': next_period,
    })
    return render_to_response('chuzuwu/room-record-index.html',
                              context_instance=context)


@login_required
def room_record_add(request):
    period_options = Period.objects.all().order_by('-period')
    room_options = Room.objects.all().order_by('number')
    if request.method == 'POST':
        datas = request.POST.copy()
        # 设置房间状态
        room_id = datas.get('room')
        tenant_id = datas.get('tenant')
        if room_id != '':
            room_id = int(room_id)
        if tenant_id != '':
            tenant_id = int(tenant_id)
        tenant = Tenant.objects.get(id=tenant_id)
        room = Room.objects.get(id=room_id)
        room.status = 'L'
        room.tenant = tenant
        # room.rent = int(datas.get('rent'))
        room.save()

        datas.setlist('rent', [unicode(room.rent)])
        form = RoomRecordForm(datas)
        if form.is_valid():
            form.save()
        else:
            messages.error(request, '添加不成功')
        return redirect(reverse('room_record'))

    tenant_options = Tenant.objects.all()
    room_record_form = RoomRecordForm()
    context = RequestContext(request, {
        'record_form': room_record_form,
        'tenant_options': tenant_options,
        'room_options': room_options,
        'period_options': period_options,
    })
    return render_to_response('chuzuwu/room-record-add.html',
                              context_instance=context)


@login_required
def room_record_update(request, rid):
    try:
        room_record = RoomRecord.objects.get(id=rid)
    except Record.DoesNotExist:
        print 'error'
    if request.method == 'POST':
        datas = request.POST
        # 设置房间状态
        room_id = datas.get('room')
        tenant_id = datas.get('tenant')
        if room_id != '':
            room_id = int(room_id)
        if tenant_id != '':
            tenant_id = int(tenant_id)
        tenant = Tenant.objects.get(id=tenant_id)
        room = Room.objects.get(id=room_id)
        is_room_back = datas.get('is_room_deposit_back')
        if is_room_back:
            # 设置room状态
            room.status = 'E'
            room.tenant = None
        else:
            room.tenant = tenant
        room.rent = int(datas.get('rent'))
        room.save()

        form = RoomRecordForm(datas, instance=room_record)
        if form.is_valid():
            form.save()
        else:
            messages.error(request, '更新不成功')
        return redirect(reverse('room_record'))

    tenant_options = Tenant.objects.all()
    period_options = Period.objects.all().order_by('-period')
    room_record_form = RoomRecordForm()
    context = RequestContext(request, {
        'record': room_record,
        'record_form': room_record_form,
        'tenant_options': tenant_options,
        'period_options': period_options,
    })
    return render_to_response('chuzuwu/room-record-update.html',
                              context_instance=context)


@login_required
def download_record(request, pid):
    pid = int(pid)
    period = Period.objects.get(id=pid)
    records = Record.objects.filter(period=period).order_by('room__number')\
        .select_related('room', 'period', 'tenant')
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('sheet1')
    col_len = len(EXCEL_RECORD_COL)
    sheet.write_merge(0, 0, 0, col_len-1, unicode(period))
    for i in range(col_len):
        sheet.write(1, i, EXCEL_RECORD_COL[i])
    # 简单统计
    record_count = {
        'number': u'合计',
        'rent': 0,
        'electric': 0,
        'internet': 0,
        'charge': 0,
        'tv': 0,
        'last_total': 0,
        'total': 0,
        # 'num_no_money': 0,
    }
    # 统计 and 写入数据
    for j in range(len(records)):
        record_count['rent'] += records[j].rent_fee
        record_count['electric'] += records[j].electric_fee
        record_count['internet'] += records[j].internet_fee
        record_count['charge'] += records[j].charge_fee
        record_count['tv'] += records[j].tv_fee
        record_count['total'] += records[j].total_fee
        # if not records[j].is_get_money:
        #     record_count['num_no_money'] += 1

        x = j+2
        sheet.write(x, 0, records[j].room.number)
        sheet.write(x, 1, unicode(records[j].tenant) if records[j].tenant is not None else '')
        sheet.write(x, 2, records[j].rent_fee if records[j].rent_fee != 0 else '')
        sheet.write(x, 3, records[j].electric_fee if records[j].electric_fee != 0 else '')
        sheet.write(x, 4, records[j].internet_fee if records[j].internet_fee != 0 else '')
        sheet.write(x, 5, records[j].charge_fee if records[j].charge_fee != 0 else '')
        sheet.write(x, 6, records[j].total_fee if records[j].total_fee != 0 else '')
        # 如果没给钱，设置style颜色
        # sheet.write(x, 7, '' if records[j].is_get_money else u'没给钱')
        sheet.write(x, 7, unicode(records[j].remark))
        if (j+1) % 12 == 0:
            number_total = record_count['total'] - record_count['last_total']
            sheet.write(x, 8, number_total)
            record_count['last_total'] = record_count['total']
    # 写入最后一行统计信息
    rownum = len(records) + 2
    sheet.write(rownum, 0, record_count['number'])
    sheet.write(rownum, 2, record_count['rent'])
    sheet.write(rownum, 3, record_count['electric'])
    sheet.write(rownum, 4, record_count['internet'])
    sheet.write(rownum, 5, record_count['charge'])
    sheet.write(rownum, 6, record_count['tv'])
    sheet.write(rownum, 7, record_count['total'])
    # sheet.write(rownum, 8, u'没给钱的有%s个' % record_count['num_no_money'])
    sheet.write(rownum, 8, record_count['total'])
    # 保存到本地
    file_name = '%s.xls' % period.period.strftime('%Y-%m')
    file_fullname = EXCEL_PATH + '/record/' + file_name
    workbook.save(file_fullname)

    # 实现下载
    response = StreamingHttpResponse(file_iterator(file_fullname))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
    return response


@login_required
def upload_record(request):
    if request.method == 'POST':
        file = request.FILES['file']
        path = EXCEL_PATH + '/record/import/'
        handle_upload_record_file(file, path)
        # 读取文件内容到数据库
        period_year = int(file.name.split('-')[0])
        period_month = int(file.name.split('-')[1].split('.')[0])
        cur_date = module_date(period_year, period_month, 1)
        period, created = Period.objects.get_or_create(period=cur_date)
        house = House.objects.first()

        workbook = xlrd.open_workbook(path + file.name)
        sheet = workbook.sheet_by_index(0)
        for rownum in range(2, sheet.nrows-1):
            # 每一行格式[房号，租金，电费，网费，充电，小计，备注]
            room_number = int(sheet.row_values(rownum)[0])
            room, created = Room.objects.get_or_create(number=room_number,
                                                       house=house)
            record = Record(period=period, room=room)
            # TODO 判断是否数字
            if sheet.row_values(rownum)[1] != '':
                record.rent_fee = int(sheet.row_values(rownum)[1])
            if sheet.row_values(rownum)[2] != '':
                record.electric_fee = float(sheet.row_values(rownum)[2])
            if sheet.row_values(rownum)[3] != '':
                record.internet_fee = int(sheet.row_values(rownum)[3])
            if sheet.row_values(rownum)[4] != '':
                record.charge_fee = int(sheet.row_values(rownum)[4])
            if sheet.row_values(rownum)[5] != '':
                record.total_fee = float(sheet.row_values(rownum)[5])
            record.remark = sheet.row_values(rownum)[6]
            record.save()
        messages.success(request, '导入成功')
    context = RequestContext(request, {})
    return render_to_response('chuzuwu/upload-record.html',
                              context_instance=context)


@login_required
def leave_room(request, rid):
    room = get_object_or_404(Room, pk=int(rid))
    return_data = {'room_number': room.number}
    if room.status == 'E':
        return_data.update(RETURN_MSG['room_empty'])
        return HttpResponse(json.dumps(return_data),
                            content_type="application/json")
    else:
        room_records = RoomRecord.objects.filter(room=room).order_by('-move_in_date')
        if room_records.count() == 0:
            return_data.update(RETURN_MSG['room_record_not_found'])
            return HttpResponse(json.dumps(return_data),
                                content_type="application/json")
        else:
            room_record = room_records[0]
            if room_record.is_finish():
                return_data.update(RETURN_MSG['room_record_finish'])
                return HttpResponse(json.dumps(return_data),
                                    content_type="application/json")
            else:
                room_record.move_out_date = module_date.today()
                tasks = []
                if not room_record.is_room_deposit_back and room_record.room_deposit != 0:
                    tasks.append('退回押金：¥{0}'.format(room_record.room_deposit))
                if not room_record.is_promise_deposit_back and room_record.promise_deposit != 0:
                    tasks.append('退回订金：¥{0}'.format(room_record.promise_deposit))
                if not room_record.is_tv_deposit_back and room_record.tv_deposit != 0:
                    tasks.append('退回电视机顶盒押金：¥{0}'.format(room_record.tv_deposit))
                room_record.is_promise_deposit_back = True
                room_record.is_room_deposit_back = True
                room_record.is_tv_deposit_back = True
                room_record.save()
                return_data.update(RETURN_MSG['success'])
                return_data.update({'tasks': tasks})
    room.status = 'E'
    room.save()
    return HttpResponse(json.dumps(return_data),
                        content_type="application/json")


@login_required
def enter_room(request, rid):
    # 暂时没用
    room = get_object_or_404(Room, pk=int(rid))
    return_data = {'room_number': room.number}
    if room.status == 'L':
        return_data.update(RETURN_MSG['room_lived'])
        return HttpResponse(json.dumps(return_data, separator=(',', ':')),
                                       content_type="application/json")
    else:
        datas = json.loads(request.POST['datas'])
        period_id = int(datas['period_id'])
        tenant_id = int(datas['tenant_id'])
        # rent 从room获取
        room_deposit = int(datas['room_deposit'])
        promise_deposit = int(datas['promise_deposit'])
        tv_deposit = int(datas['tv_deposit'])
        remark = int(datas['remark'])
        period, created = get_object_or_404(Period, pk=period_id)
        tenant, created = get_object_or_404(Tenant, pk=tenant_id)
        room_record = RoomRecord.objects.create(
            room=room,
            period=period,
            tenant=tenant,
            rent=room.rent,
            room_deposit=room_deposit,
            promise_deposit=promise_deposit,
            tv_deposit=tv_deposit,
            move_in_date=module_date.today(),
            remark=remark
        )
        return_data.update(RETURN_MSG['success'])
    room.status = 'L'
    room.save()
    return HttpResponse(json.dumps(return_data, separator=(',', ':')),
                                   content_type="application/json")
