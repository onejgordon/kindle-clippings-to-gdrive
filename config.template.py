# -*- coding: utf-8 -*-

'''
Configuration settings
'''

TARGET = "gsheets"  # Or "flow" via http://flowdash.co
FLOW_USER_ID = 0
FLOW_USER_PW = ""
GOOGLE_SHEET_KEY = ""
INCLUDE_TYPES = ['highlight'] # ['note', 'bookmark']
SHEET_COLUMNS = {
    'hash': 0,
    'type': 1,
    'quote': 2,
    'source': 3,
    'location': 4,
    'date': 5
}
DELETE_ON_KINDLE_AFTER_UPLOAD = False