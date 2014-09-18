# -*- coding: UTF-8 -*-
# Copyright 2013 Luc Saffre
# License: BSD (see file COPYING for details)

from decimal import Decimal
from django.utils.translation import ugettext_lazy as _
from lino import ad


class Plugin(ad.Plugin):
    verbose_name = _("VAT")

    vat_quarterly = False
    """
    Set this to True to support quarterly VAT declarations.
    Used by :mod:`lino.modlib.declarations`
    """

    def get_vat_class(self, tt, item):
        return 'normal'

    VAT_CLASS_TO_RATE = dict(
        exempt=Decimal(),
        reduced=Decimal('0.07'),
        normal=Decimal('0.20')
    )

    def get_vat_rate(self, tt, vc, vr):
        return self.VAT_CLASS_TO_RATE[vc.name]
