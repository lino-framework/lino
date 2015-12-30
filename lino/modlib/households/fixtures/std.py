# -*- coding: UTF-8 -*-
# Copyright 2012-2014 Luc Saffre
# License: BSD (see file COPYING for details)
"""
The `std` fixture for `households`
==================================

Adds some :class:`household roles <households.Role>`.

"""

from django.utils.translation import ugettext_lazy as _

from lino.api import dd, rt


def objects():
    Type = rt.modules.households.Type

    yield Type(**dd.str2kw('name', _("Married couple")))
    # Verheiratet / Marié

    yield Type(**dd.str2kw('name', _("Divorced couple")))
    # Geschieden / Divorcé

    yield Type(**dd.str2kw('name', _("Factual household")))
    # Faktischer Haushalt / Ménage de fait

    yield Type(**dd.str2kw('name', _("Legal cohabitation")))
    # Legale Wohngemeinschaft / Cohabitation légale

    yield Type(**dd.str2kw('name', _("Isolated")))
    yield Type(**dd.str2kw('name', _("Other")))
