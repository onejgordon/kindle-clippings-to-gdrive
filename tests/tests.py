# -*- coding: utf-8 -*-
import csv
import os
import shutil
import unittest
from collections import defaultdict
from datetime import datetime

import clippings
from script.config import CSV_OUTPUT_DIR
from script.push_clippings import PushClippings


# noinspection SpellCheckingInspection
class PushTests(unittest.TestCase):
    def setUp(self):
        self.clip_datas = None
        global push
        push = PushClippings()

    def _get_clip_datas(self):
        #  From https://github.com/coolharsh55/klip
        if not self.clip_datas:
            clip_datas = []

            # kindle paperwhite
            clip_data = PushClippings.process_notes(raw=clippings.Paperwhite, kindle="Paperwhite")
            clip_datas.append(clip_data)

            # old gen kindles
            clip_data = PushClippings.process_notes(raw=clippings.OldGenKindle, kindle="OldGenKindle")
            clip_datas.append(clip_data)

            # kindle touch
            clip_data = PushClippings.process_notes(raw=clippings.Touch, kindle="Touch")
            clip_datas.append(clip_data)

            # kindle 4
            clip_data = PushClippings.process_notes(raw=clippings.Kindle4, kindle="Kindle4")
            clip_datas.append(clip_data)

            self.clip_datas = clip_datas

        return self.clip_datas

    def test_load(self):
        #  From https://github.com/coolharsh55/klip
        clip_datas = self._get_clip_datas()
        for _clip_data in clip_datas:
            # type control
            assert isinstance(_clip_data, dict), "invalid type for clip_data"

        # len control
        self.assertEqual(len(clip_datas[0]), 3)
        self.assertEqual(len(clip_datas[1]), 4)
        self.assertEqual(len(clip_datas[2]), 2)
        self.assertEqual(len(clip_datas[3]), 2)

    def test_parsing(self):
        # From https://github.com/coolharsh55/klip
        clip_datas = self._get_clip_datas()

        for item in clip_datas[0].values():
            assert (item["title"] in [
                "The Mythical Man Month",
                "Two Scoops of Django: Best Practices for Django 1.5"])

        for item in clip_datas[1].values():
            assert (item["title"] in [
                "Learning_Python_Fourth_Edition",
                "Learning_Python_Second_Edition"])

        for item in clip_datas[2].values():
            assert (item["title"] in [
                "Regular Expressions Cookbook",
                "Das Kapital"])

        for item in clip_datas[3].values():
            assert (item["title"] in ["Dubliners", "Lab Girl"])

    def test_CSV(self):
        clip_datas = self._get_clip_datas()
        push.save_csv(clip_datas[0])
        file_name = CSV_OUTPUT_DIR + "\kindle-notes-loaded-%s.csv" % datetime.strftime(datetime.now(), "%Y-%m-%d-%H-%M")

        self.assertTrue(os.path.isfile(file_name), "CSV not saved correctly.")
        self.assertTrue(os.path.getsize(file_name) > 0, "CSV saved but empty.")

        columns = defaultdict(list)

        # From https://stackoverflow.com/a/16503661/1649917
        with open(file_name) as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                for (k, v) in row.items():
                    columns[k].append(v)

        for count, item in enumerate(clip_datas[0]):
            # Check all ID's are in file.
            self.assertTrue(columns['id'][count] == item)

        # Delete created CSV files
        shutil.rmtree(CSV_OUTPUT_DIR)

    def test_gdrive(self):
        clip_datas = self._get_clip_datas()
        push.push_to_gdrive(clip_datas[0])

    def test_flow(self):
        clip_datas = self._get_clip_datas()
        push.save_to_flow(clip_datas[0])


if __name__ == '__main__':
    unittest.main()
