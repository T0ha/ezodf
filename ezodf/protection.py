#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: protection routines
# Created: 20.01.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

import random

FNCHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

def random_protection_key(count=12):
    return random.sample(FNCHARS, count)