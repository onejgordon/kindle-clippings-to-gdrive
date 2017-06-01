# -*- coding: utf-8 -*-

'''
push_clippings.py

Collect notes/highlights/bookmarks from Kindle (attached via USB) to
a Google Spreadsheet, and optionally save CSV on local machine

Supports: highlights, notes

TODO: Dont distribute client_secrets

'''

import hashlib
import klip
from datetime import datetime
import csv
from google_credentials_helper import GoogleCredentialHelper
from config import GOOGLE_SHEET_KEY, INCLUDE_TYPES, SHEET_COLUMNS, \
    TARGET, DELETE_ON_KINDLE_AFTER_UPLOAD, DO_UPLOAD, SAVE_CSV_BACKUP, \
    DIRECTORY, NOTES_FILE, CSV_OUTPUT_DIR, KINDLE_NOTE_SEP, DEVICE
import re
import os
import io
import sys
import getopt
import util
import requests
import base64


class PushClippings(object):
    def __init__(self, file_override=None):
        self.source_file = file_override if file_override else \
            DIRECTORY + NOTES_FILE

    def load_notes_from_kindle(self):
        data = None
        try:
            with io.open(self.source_file, mode="r", encoding="utf8") as f:
                data = f.read()
        except IOError, e:
            print "Cant find source - Kindle not plugged in?"
        else:
            print "Loaded data, length: %d" % len(data)
        return data

    @staticmethod
    def process_notes(raw, kindle=DEVICE):
        dict = {}
        processed = klip.load(raw, kindle)
        for item in processed:
            item_md5 = hashlib.md5(item["content"])
            item_hash = item_md5.hexdigest()
            dict[item_hash] = item
            print "Processed %d note(s)" % len(dict.keys())
        return dict

    def push_to_gdrive(self, processed_notes):
        print "Fetching existing clippings from Google Drive..."
        # Read from quote sheet to get all hashes
        ghelper = GoogleCredentialHelper('sheets', 'v4')
        service = ghelper.get_service()
        if service:
            result = service.spreadsheets().values().get(
                spreadsheetId=GOOGLE_SHEET_KEY,
                majorDimension="COLUMNS",
                range='A:A').execute()
            # Write missing hashes to spreadsheet
            existing_hashes = []
            values = result.get('values')
            if values:
                rows = values[0]
                n_rows = len(rows) - 1
                if n_rows > 0:
                    existing_hashes = rows[1:]
            if DO_UPLOAD:
                print "Uploading missing clippings to Google Drive..."
                put_values = []
                for hash, note in processed_notes:
                    if hash in existing_hashes:
                        print "Skipping item already in sheet - %s" % hash
                    else:
                        _type = note["type"]
                        if _type.lower() in INCLUDE_TYPES:
                            # Space by col indexes?
                            row = [None for x in range(max(SHEET_COLUMNS.values()) + 1)]
                            for prop, index in SHEET_COLUMNS.items():
                                if prop == 'hash':
                                    row[index] = hash
                                else:
                                    row[index] = note.get(prop)
                            put_values.append(row)
                if put_values:
                    body = {
                        'values': put_values
                    }
                    result = service.spreadsheets().values().append(
                        spreadsheetId=GOOGLE_SHEET_KEY,
                        range="A:A",
                        valueInputOption="RAW",
                        insertDataOption="INSERT_ROWS", body=body).execute()
                    if result:
                        print "Updated %s row(s)!" % result.get('updates', {}).get('updatedRows', "?")
                else:
                    print "Nothing to put"

    def save_to_flow(self, processed_notes):
        if DO_UPLOAD:
            print "Uploading clippings to Flow Dashboard..."
            successful = 0
            from config import FLOW_USER_EMAIL, FLOW_USER_PW
            encoded = base64.b64encode("%s:%s" % (FLOW_USER_EMAIL, FLOW_USER_PW))
            headers = {"authorization": "Basic %s" % encoded}
            for hash, note in processed_notes.items():
                _type = note["type"]
                if _type.lower() in INCLUDE_TYPES:
                    params = {
                        'source': note["title"],
                        'content': note["content"],
                        'location': note["page"],
                        'date': note["added_on"]
                    }
                    r = requests.post("http://flowdash.co/api/quote",
                                      params=params,
                                      headers=headers)
                    if r.status_code == 200:
                        res = r.json()
                        if res and res.get('success'):
                            successful += 1
                            q = res.get('quote')
                            if q:
                                print "Successfully uploaded quote to Flow with id %s" % q.get('id')
            print "Updated %s row(s)!" % successful

    def save_csv(self, notes):
        directory = CSV_OUTPUT_DIR
        if not os.path.exists(directory):
            os.makedirs(directory)
        fname = "kindle-notes-loaded-%s.csv" % \
                datetime.strftime(datetime.now(), "%Y-%m-%d-%H:%M")
        with open("Kindle.csv", 'w+') as f:
            writer = csv.DictWriter(f, fieldnames=['id', 'type', 'quote', 'source', 'location', 'date']
                                    , extrasaction='ignore')
            writer.writeheader()
            for hash, note in notes.items():
                note['id'] = hash
                note['type'] = note["meta"]["type"]
                note['quote'] = note["content"]
                note['source'] = note["title"] + " (" + note["author"] + ")"
                if note["meta"]["page"] is not None:
                    note['location'] = str(note["meta"]["page"]) + " " + str(note["meta"]["location"])
                else:
                    note['location'] = str(note["meta"]["location"])
                note['date'] = str(note["added_on"])
                writer.writerow(note)
            f.close()

    def remove_source(self):
        print "Deleting %s..." % self.source_file
        os.remove(self.source_file)
        print "Deleted."

    def run(self):
        raw_notes = self.load_notes_from_kindle()
        if raw_notes:
            processed_notes = self.process_notes(raw_notes)
            if TARGET == "gsheet":
                self.push_to_gdrive(processed_notes)
            elif TARGET == "flow":
                self.save_to_flow(processed_notes)
            if self.SAVE_CSV_BACKUP:
                self.save_csv(processed_notes)
            if self.DELETE_ON_KINDLE_AFTER_UPLOAD:
                self.remove_source()
        print "Done"


if __name__ == "__main__":
    argv = sys.argv[1:]
    HELP = 'push_clippings.py [-h] [--file=/Users/.../Clippings.txt]'
    try:
        opts, args = getopt.getopt(argv, "hf:", ["file="])
    except getopt.GetoptError:
        print HELP
        sys.exit(2)
    # Defaults
    file_override = None
    for opt, arg in opts:
        if opt == '-h':
            print HELP
            sys.exit()
        elif opt in ("-f.json", "--file") and arg:
            file_override = arg

    push = PushClippings(file_override=file_override)
    push.run()
