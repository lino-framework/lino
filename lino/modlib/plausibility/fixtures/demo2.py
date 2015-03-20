# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""Runs the :manage:`check_plausibility` management command.

"""

from lino.api import rt


def objects():
    rt.modules.plausibility.check_plausibility()
    return []
