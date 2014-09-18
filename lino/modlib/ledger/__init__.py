# -*- coding: UTF-8 -*-
# Copyright 2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""

.. setting:: ledger.use_pcmn

Whether to use the PCMN notation.

PCMN stands for "plan compatable minimum normalisé" and is a
standardized nomenclature for accounts used in France and Belgium.

"""

from __future__ import unicode_literals


from django.utils.translation import ugettext_lazy as _

from lino import ad


class Plugin(ad.Plugin):
    verbose_name = _("Ledger")
    use_pcmn = False
