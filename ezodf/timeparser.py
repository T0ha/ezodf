#!/usr/bin/env python
#coding:utf-8
# Author:  mozman -- <mozman@gmx.at>
# Purpose: timeparser
# Created: 29.01.2011
# Copyright (C) , Manfred Moitzi
# License: GPLv3

import re
import math
from datetime import date, timedelta, datetime

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"
DATE_FORMAT = "%Y-%m-%d"

class TimeParser:
    duration_matcher = re.compile("^P(\d+Y)?(\d+M)?(\d+D)?(?:T(\d+H)?(\d+M)?(\d+(?:,\d+)?S)?)?$")

    def __init__(self, time):
        if isinstance(time, str):
            self.timestr = time
            self.value = TimeParser.parse(time)
        else:
            self.value = time
            self.timestr = str(self)

    def __str__(self):
        if self.is_date:
            if self.has_time:
                string = self.value.strftime(DATETIME_FORMAT)
            else:
                string = self.value.strftime(DATE_FORMAT)
        else:
            string = TimeParser.duration_to_string(self.value)
        return string

    @staticmethod
    def parse(timestr):
        if timestr.startswith('P'):
            value = TimeParser.duration_parser(timestr)
        else:
            if 'T' in timestr:
                value = datetime.strptime(timestr, DATETIME_FORMAT)
            else:
                value = datetime.strptime(timestr, DATE_FORMAT).date()
        return value

    @property
    def is_date(self):
        return isinstance(self.value, date)

    @property
    def has_time(self):
        return isinstance(self.value, datetime)

    @property
    def is_duration(self):
        return isinstance(self.value, timedelta)

    @staticmethod
    def duration_parser(duration):
        def clean(timepart):
            result = 0
            if timepart:
                timepart = timepart[:-1].replace(',', '.')
                result = float(timepart)
            return result

        matchresult = TimeParser.duration_matcher.match(duration)
        if matchresult:
            timeparts = [clean(part) for part in matchresult.groups()]
            years, months, days, hours, minutes, seconds = timeparts
            days = years * 365 + months * 30 + days
        else:
            raise ValueError('not a valid duration: %s' % duration)
        return timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)

    @staticmethod
    def duration_to_string(duration):
        def get_time(seconds):
            hours = int(seconds / 3600)
            seconds = seconds % 3600
            minutes = int(seconds / 60)
            seconds = seconds % 60
            return (hours, minutes, seconds)

        timeparts = ["P%dD" % duration.days] if duration.days else ["P"]
        timeparts.append("T%02dH%02dM%02d" % get_time(duration.seconds))
        micros = duration.microseconds
        if micros > 0:
            micros_str = ",%06d" % micros
            timeparts.append("%sS" % micros_str[:5])
        else:
            timeparts.append("S")

        return ''.join(timeparts)
