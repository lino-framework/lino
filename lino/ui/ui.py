# -*- coding: UTF-8 -*-
# Copyright 2009-2013 Luc Saffre
# License: BSD (see file COPYING for details)

def parse_bool(s):
    return s == 'true'


def parse_int(s, default=None):
    if s is None:
        return None
    return int(s)
