# -*- coding: UTF-8 -*-
# Copyright 2017-2018 Luc Saffre
# License: BSD (see file COPYING for details)
"""Runs the :manage:`checksummaries` management command.

"""

from django.core.management import call_command


def objects():
    call_command('checksummaries')
    return []
