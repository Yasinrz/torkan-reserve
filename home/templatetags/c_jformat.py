from django import template
from jalali_date import date2jalali

register = template.Library()

@register.filter
def to_jalali(value):
    if value:
        return date2jalali(value).strftime('%Y/%m/%d')
    return ""

@register.filter
def to_rial(value):
    
    try:
        return "{:,}".format(int(value))
    except (ValueError, TypeError):
        return value