# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""
Defines Lino specific exceptions
"""


class ChangedAPI(Exception):
    """protect against non-converted legacy code"""
    pass
