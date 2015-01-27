#!/usr/bin/env python
#coding:utf-8
# Purpose: test timeparser
# Created: 29.01.2011
# Copyright (C) , Manfred Moitzi
# License: MIT license
from __future__ import unicode_literals, print_function, division
__author__ = "mozman <mozman@gmx.at>"

# Standard Library
try:
    import unittest2 as unittest
except ImportError:
    import unittest
from datetime import timedelta, date, datetime

# objects to test
from ezodf.timeparser import TimeParser

class TestTimeParser(unittest.TestCase):
    def test_init_as_class(self):
        p = TimeParser('2000-01-01')
        self.assertIsNotNone(p)

class TestDurationParser(unittest.TestCase):
    def test_just_days(self):
        result = TimeParser.duration_parser("P7D")
        expected = timedelta(days=7)
        self.assertEqual(result, expected)

    def test_just_hours(self):
        result = TimeParser.duration_parser("PT1H")
        expected = timedelta(hours=1)
        self.assertEqual(result, expected)

    def test_just_minutes(self):
        result = TimeParser.duration_parser("PT1M")
        expected = timedelta(minutes=1)
        self.assertEqual(result, expected)

    def test_just_seconds(self):
        result = TimeParser.duration_parser("PT1S")
        expected = timedelta(seconds=1)
        self.assertEqual(result, expected)

    def test_just_seconds_frac(self):
        result = TimeParser.duration_parser("PT1,50S")
        expected = timedelta(seconds=1.5)
        self.assertEqual(result, expected)

    def test_mix_min_sec_frac(self):
        result = TimeParser.duration_parser("PT5M1,50S")
        expected = timedelta(minutes=5, seconds=1.5)
        self.assertEqual(result, expected)

    def test_mix_hrs_min_sec_frac(self):
        result = TimeParser.duration_parser("PT2H5M1,50S")
        expected = timedelta(hours=2, minutes=5, seconds=1.5)
        self.assertEqual(result, expected)

    def test_mix_hrs_min_sec(self):
        result = TimeParser.duration_parser("PT02H05M01S")
        expected = timedelta(hours=2, minutes=5, seconds=1)
        self.assertEqual(result, expected)

    def test_mix_hrs_min(self):
        result = TimeParser.duration_parser("PT02H05M")
        expected = timedelta(hours=2, minutes=5)
        self.assertEqual(result, expected)

    def test_parse_error(self):
        with self.assertRaises(ValueError):
            TimeParser.duration_parser("T02H05M")

class TestDurationToString(unittest.TestCase):
    def test_just_days(self):
        result = TimeParser.duration_to_string(timedelta(days=7))
        self.assertEqual(result, 'P7DT00H00M00S')

    def test_just_hours(self):
        result = TimeParser.duration_to_string(timedelta(hours=7))
        self.assertEqual(result, 'PT07H00M00S')

    def test_just_minutes(self):
        result = TimeParser.duration_to_string(timedelta(minutes=7))
        self.assertEqual(result, 'PT00H07M00S')

    def test_just_seconds(self):
        result = TimeParser.duration_to_string(timedelta(seconds=7))
        self.assertEqual(result, 'PT00H00M07S')

    def test_seconds_frac(self):
        result = TimeParser.duration_to_string(timedelta(seconds=1.17))
        self.assertEqual(result, 'PT00H00M01,1700S')

    def test_days_hours_min_sec_frac(self):
        result = TimeParser.duration_to_string(timedelta(days=7, hours=5, minutes=45, seconds=1.789))
        self.assertEqual(result, 'P7DT05H45M01,7890S')

class TestDate(unittest.TestCase):
    def test_is_date(self):
        p = TimeParser('2000-01-01')
        self.assertTrue(p.is_date)
        self.assertFalse(p.has_time)

    def test_parse_error_no_days(self):
        with self.assertRaises(ValueError):
            TimeParser.parse('2000-01')

    def test_parse_error_no_months(self):
        with self.assertRaises(ValueError):
            TimeParser.parse('2000')

    def test_date_value(self):
        p = TimeParser('2000-01-01')
        self.assertEqual(p.value, date(2000, 1, 1))

    def test_to_string(self):
        p = TimeParser('2000-01-01')
        self.assertEqual(str(p), '2000-01-01')

class TestDateTime(unittest.TestCase):
    def test_is_datetime(self):
        p = TimeParser('2000-01-01T12:00:00')
        self.assertTrue(p.is_date)
        self.assertTrue(p.has_time)

    def test_parse_error_no_seconds(self):
        with self.assertRaises(ValueError):
            TimeParser.parse('2000-01-01T12:00')

    def test_parse_error_no_minutes(self):
        with self.assertRaises(ValueError):
            TimeParser.parse('2000-01-01T12')

    def test_datetime_value(self):
        p = TimeParser('2000-01-01T12:00:00')
        self.assertEqual(p.value, datetime(2000, 1, 1, 12))

    def test_to_string(self):
        p = TimeParser('2000-01-01T12:00:00')
        self.assertEqual(str(p), '2000-01-01T12:00:00')

class TestTimedelta(unittest.TestCase):
    def test_is_time(self):
        p = TimeParser('PT00H05M00,0000S')
        self.assertTrue(p.is_duration)

    def test_time_value_5min(self):
        p = TimeParser('PT0H05M00,0000S')
        self.assertEqual(p.value, timedelta(minutes=5))

    def test_time_value_1hr(self):
        p = TimeParser('PT1H00M00,0000S')
        self.assertEqual(p.value, timedelta(hours=1))

    def test_to_string(self):
        p = TimeParser('PT1H00M00,0000S')
        self.assertEqual(str(p), 'PT01H00M00S')

class TestSetTimeObjects(unittest.TestCase):
    def test_set_timedelta(self):
        p = TimeParser(timedelta(minutes=5))
        self.assertEqual('PT00H05M00S', str(p))

    def test_set_date(self):
        p = TimeParser(date(2011, 2, 5))
        self.assertEqual('2011-02-05', str(p))

    def test_set_datetime(self):
        p = TimeParser(datetime(2011, 2, 5, 12, 0, 0))
        self.assertEqual('2011-02-05T12:00:00', str(p))

if __name__=='__main__':
    unittest.main()
