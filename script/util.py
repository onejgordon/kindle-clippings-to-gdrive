# -*- coding: utf-8 -*-

import unicodedata


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

