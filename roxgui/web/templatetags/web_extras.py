from django.template.defaulttags import register


@register.filter
def get_value(dic, key):
    return dic.get(key)
