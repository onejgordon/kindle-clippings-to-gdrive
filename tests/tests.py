# -*- coding: utf-8 -*-

import unittest
import samples
import clippings
from script import config, util
from script.push_clippings import PushClippings


# noinspection SpellCheckingInspection
class PushTests(unittest.TestCase):
    def setUp(self):
        self.clip_datas = None

    def _get_clip_datas(self):
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
        clip_data = self._get_clip_datas()

        for item in clip_data[0].values():
            assert (item["title"] in [
                "The Mythical Man Month",
                "Two Scoops of Django: Best Practices for Django 1.5"])


if __name__ == '__main__':
    unittest.main()
