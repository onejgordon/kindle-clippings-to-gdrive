# -*- coding: utf-8 -*-

import unittest
from os import sys, path
sys.path.append(path.dirname(path.dirname(__file__)))
import samples
from push_clippings import PushClippings
import util


class PushTests(unittest.TestCase):

    def test_parsing_dates(self):
        volley = [
            ('Friday, April 22, 2016 1:43:50 AM', '2016-04-22 01:43:50'),
            ('Friday, December 30, 2016 7:47:36 PM', '2016-12-30 19:47:36')
        ]
        for v in volley:
            raw, expected = v
            dt = util.parse_kindle_time(raw)
            out = util.print_datetime(dt)
            self.assertEqual(out, expected)

    def test_parsing_notes(self):
        volley = [
            (
                samples.SU_1,
                (
                    "Surfing Uncertainty: Prediction, Action, and the Embodied Mind (Clark, Andy)",
                    "Highlight",
                    "page 70 | Location 1613-1616",
                    "2016-04-13 22:39:18"
                )
            ),
            (
                samples.SOTHB_1,
                (
                    "The Story of the Human Body (Daniel Lieberman)",
                    "Highlight",
                    "Location 2479-2481",
                    "2017-01-03 17:54:18"
                )
            )

        ]
        push = PushClippings()
        for v in volley:
            text, result_tuple = v
            source, type, location, date = result_tuple
            result = push._parse_note(text)
            print result
            self.assertIsNotNone(result)
            self.assertEqual(source, result.get('source'))
            self.assertEqual(type, result.get('type'))
            self.assertEqual(location, result.get('location'))
            self.assertEqual(date, result.get('date'))
            self.assertTrue(len(result.get('quote')) > 0)

    def test_parsing_raw(self):
        raw = samples.RAW
        push = PushClippings()
        raw_split = raw.split(PushClippings.KINDLE_NOTE_SEP)
        self.assertEqual(len(raw_split), 86)

        first_parsed = push._parse_note(raw_split[0])
        self.assertIsNotNone(first_parsed)

if __name__ == '__main__':
    unittest.main()