# -*- coding: UTF-8 -*-
# Copyright 2013-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""The :mod:`lino.modlib.vat` package provides models and business
logic for handling value-added tax (VAT).

This module is designed to work both *with* and *without*
:mod:`lino.modlib.ledger` and :mod:`lino.modlib.declarations`
installed.



.. autosummary::
   :toctree:

    models
    utils
    fixtures.euvatrates



See :mod:`ml.vat`.

"""

from django.utils.translation import ugettext_lazy as _
from lino import ad


class Plugin(ad.Plugin):
    """
    Extends :class:`lino.core.plugin.Plugin`. See also :doc:`/dev/ad`.
    """
    verbose_name = _("VAT")

    vat_quarterly = False
    """
    Set this to True to support quarterly VAT declarations.
    Used by :mod:`ml.declarations`.
    """

    default_vat_regime = 'private'
    default_vat_class = 'normal'

    country_code = None
    """The 2-letter ISO code of the country where the site owner is
    located.  This may not be empty, and there must be a country with
    that ISO code in :class:`lino.modlib.countries.models.Country`.

    """

    def get_vat_class(self, tt, item):
        return 'normal'

    def get_country(self):
        return self.site.modules.countries.Country.objects.get(
            pk=self.country_code)

    def on_site_startup(self, site):
        if self.country_code is None:
            raise Exception(
                "VAT plugin requires nonempty `country_code` setting.")
        vat = site.modules.vat
        if isinstance(self.default_vat_regime, basestring):
            self.default_vat_regime = vat.VatRegimes.get_by_name(
                self.default_vat_regime)
        if isinstance(self.default_vat_class, basestring):
            self.default_vat_class = vat.VatClasses.get_by_name(
                self.default_vat_class)
