from django.template.defaulttags import register
import logging

@register.filter
def get_value(dic, key):
    return dic.get(key)