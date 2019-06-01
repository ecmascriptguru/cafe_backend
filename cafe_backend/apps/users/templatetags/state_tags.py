from django import template
from ....core.constants.states import (
    DEFAULT_STATE, TABLE_STATE, ORDER_STATE)


register = template.Library()


@register.filter('state_text')
def state_text(instance):
    if hasattr(instance, 'state'):
        return instance.get_state_display()
    return ''


@register.filter('state_bg_color')
def state_bg_color(instance):
    color_map = {
        DEFAULT_STATE.default: 'aqua',
        DEFAULT_STATE.using: 'green',
        DEFAULT_STATE.pending: 'yellow',
        DEFAULT_STATE.rejected: 'grey',
        DEFAULT_STATE.waiting: 'yellow',
        DEFAULT_STATE.delivered: 'green',
    }

    return "bg-%s" % color_map.get(
        getattr(instance, 'state'), 'aqua')


@register.filter('table_state_bg_color')
def table_state_bg_color(instance):
    color_map = {
        ORDER_STATE.default: 'red',
        ORDER_STATE.delivered: 'green',
        ORDER_STATE.canceled: 'grey',
    }

    return "bg-%s" % color_map.get(
        getattr(instance, 'state'), 'aqua')


@register.filter('order_item_state_bg_color')
def order_item_state_bg_color(instance):
    color_map = {
        TABLE_STATE.blank: 'aqua',
        TABLE_STATE.using: 'green',
        TABLE_STATE.reserved: 'yellow',
    }

    return "bg-%s" % color_map.get(
        getattr(instance, 'state'), 'aqua')
