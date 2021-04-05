# -*- coding: UTF-8 -*-
# Copyright 2017-2018 Luc Saffre
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""Runs the :manage:`checksummaries` management command.

"""

from django.core.management import call_command


def objects():
    call_command('checksummaries')
    return []
