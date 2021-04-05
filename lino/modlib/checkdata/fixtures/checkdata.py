# -*- coding: UTF-8 -*-
# Copyright 2015 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""Runs the :manage:`checkdata` management command with `--fix`
option.

"""

from django.core.management import call_command


def objects():
    call_command('checkdata', fix=True)
    return []
