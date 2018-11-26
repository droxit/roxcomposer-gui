from django.template.defaulttags import register
import logging

@register.filter
def get_watch_toggled(dictionary, key):
    dic = dictionary['watch_button_active']
    logging.info("DICT: " + str(dic))
    return dic.get(key)