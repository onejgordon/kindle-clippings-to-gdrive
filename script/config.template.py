# -*- coding: utf-8 -*-

'''
Configuration settings
'''

TARGET = "gsheet"  # Either "flow" or "gsheet"
SAVE_CSV_BACKUP = True
CSV_OUTPUT_DIR = "output"
DO_UPLOAD = True
DELETE_ON_KINDLE_AFTER_UPLOAD = False
INCLUDE_TYPES = ['highlight']  # ['note', 'bookmark']

# Flow flow upload
FLOW_USER_EMAIL = ""
FLOW_USER_PW = ""

# For gSheet upload
GOOGLE_SHEET_KEY = ""
SHEET_COLUMNS = {
    'hash': 0,
    'type': 1,
    'quote': 2,
    'source': 3,
    'location': 4,
    'date': 5
}

# Things you may have to change depending on Kindle and OS version
DIRECTORY = "/Volumes/Kindle/documents/"
NOTES_FILE = "My Clippings.txt"
KINDLE_NOTE_SEP = "=========="

