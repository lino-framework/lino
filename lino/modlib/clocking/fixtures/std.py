# -*- coding: UTF-8 -*-
"""

"""
from __future__ import unicode_literals
from __future__ import print_function

from lino.api import rt


def objects():
    SessionType = rt.modules.clocking.SessionType
    yield SessionType(id=1, name="Default")
