# -*- coding: UTF-8 -*-
# Copyright 2013-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""See :mod:`ml.vat`."""

from decimal import Decimal
from django.utils.translation import ugettext_lazy as _
from lino import ad


class Plugin(ad.Plugin):
    verbose_name = _("VAT")

    vat_quarterly = False

    default_vat_regime = 'private'
    default_vat_class = 'normal'

    def get_vat_class(self, tt, item):
        return 'normal'

    VAT_CLASS_TO_RATE = dict(
        exempt=Decimal(),
        reduced=Decimal('0.07'),
        normal=Decimal('0.20')
    )

    def get_vat_rate(self, tt, vc, vr):
        return self.VAT_CLASS_TO_RATE[vc.name]

    def on_site_startup(self, site):
        vat = site.modules.vat
        if isinstance(self.default_vat_regime, basestring):
            self.default_vat_regime = vat.VatRegimes.get_by_name(
                self.default_vat_regime)
        if isinstance(self.default_vat_class, basestring):
            self.default_vat_class = vat.VatClasses.get_by_name(
                self.default_vat_class)
