# -*- coding: UTF-8 -*-
# Copyright 2009-2014 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
"""
Adds an arbitrary selection of a few demo languages.
"""

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from lino.utils.instantiator import Instantiator
from lino.api import dd, rt


def objects():

    Language = Instantiator('languages.Language', "id").build

    yield Language('ger', **dd.str2kw('name', _("German")))
    yield Language('fre', **dd.str2kw('name', _("French")))
    yield Language('eng', **dd.str2kw('name', _("English")))
    yield Language('dut', **dd.str2kw('name', _("Dutch")))
    yield Language('est', **dd.str2kw('name', _("Estonian")))
