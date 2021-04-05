# -*- coding: UTF-8 -*-
# Copyright 2009-2019 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""
Adds an arbitrary selection of a few languages.
"""

from __future__ import unicode_literals

from django.utils.translation import gettext_lazy as _
# from lino.utils.instantiator import Instantiator
from lino.api import dd, rt


def objects():

    # Language = Instantiator('languages.Language', "id").build

    def language(pk, iso2, name):
        kw = dict(id=pk, iso2=iso2)
        kw.update(dd.str2kw('name', name))
        return rt.models.languages.Language(**kw)

    yield language('ger', 'de', _("German"))
    yield language('fre', 'fr', _("French"))
    yield language('eng', 'en', _("English"))
    yield language('dut', 'nl', _("Dutch"))
    yield language('est', 'et', _("Estonian"))
