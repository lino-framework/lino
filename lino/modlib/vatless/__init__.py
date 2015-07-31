# -*- coding: UTF-8 -*-
# Copyright 2013-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Adds functionality for handling incoming and outgoing invoices in a
VAT-less context (i.e. for organizations which have no obligation of
VAT declaration).  Site operators subject to VATare likely to use
:mod:`lino.modlib.vat` instead.

Installing this plugin will automatically install
:mod:`lino.modlib.countries` :mod:`lino.modlib.ledger`.


.. autosummary::
   :toctree:

    mixins
    models
    ui

"""

from django.utils.translation import ugettext_lazy as _
from lino.api import ad


class Plugin(ad.Plugin):
    """See :doc:`/dev/plugins`.

    """
    verbose_name = _("VAT-less invoicing")

    needs_plugins = ['lino.modlib.countries', 'lino.modlib.ledger']

    def setup_explorer_menu(self, site, profile, m):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('vatless.Invoices')
