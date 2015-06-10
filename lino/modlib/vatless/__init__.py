# -*- coding: UTF-8 -*-
# Copyright 2013-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Adds functionality for working with invoices in a VAT-less context
(i.e. for organizations which have no obligation of VAT declaration).


.. autosummary::
   :toctree:

    models
    mixins

"""

from django.utils.translation import ugettext_lazy as _
from lino.api import ad


class Plugin(ad.Plugin):
    """See :doc:`/dev/plugins`.

    """
    verbose_name = _("VAT-less invoicing")

    needs_plugins = ['lino.modlib.countries', 'lino.modlib.ledger']

    def setup_explorer_menu(config, site, profile, m):
        m = m.add_menu(config.app_label, config.verbose_name)
        m.add_action('vatless.Invoices')

