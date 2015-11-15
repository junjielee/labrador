#!/usr/bin/env python
# encoding: utf-8

from django import template
from django.utils.translation import ugettext_lazy as _


register = template.Library()


@register.filter
def interger(figure):
    # 将float小数点后面为0的数，改为整数
    if int(figure) == figure:
        figure = int(figure)
    return figure


@register.filter
def to_blank(figure):
    # 如果为0或是None，就返回''
    if figure == 0 or figure is None:
        figure = ''
    return figure


@register.filter
def to_sex(sex):
    # M转为男，F转为女
    if sex == 'M':
        sex = '男'
    elif sex == 'F':
        sex = '女'
    return sex


@register.filter
def to_room_status(sex):
    # M转为男，F转为女
    if sex == 'L':
        sex = _('Lived')
    elif sex == 'E':
        sex = _('Empty')
    return sex
