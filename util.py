# -*- coding: utf-8 -*-

import unicodedata
from datetime import datetime


def _normalize_to_ascii(text):
    if text is None:
        return None
    normalized_text = None
    try:
        if not isinstance(text, basestring):
            text = str(text).decode('utf-8')
        elif not isinstance(text, unicode):
            text = text.decode('utf-8')
        normalized_text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore')
    except Exception, ex:
        pass
    return normalized_text


def parse_kindle_time(raw):
    '''
    Friday, April 22, 2016 1:43:50 AM
    '''
    return datetime.strptime(raw, '%A, %B %d, %Y %I:%M:%S %p')


def print_datetime(dt):
    return datetime.strftime(dt, '%Y-%m-%d %H:%M:%S')