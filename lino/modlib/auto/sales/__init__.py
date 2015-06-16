# -*- coding: UTF-8 -*-
# Copyright 2013-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""

.. autosummary::
    :toctree:

    models

"""

from lino.modlib.sales import Plugin


class Plugin(Plugin):

    extends_models = ['VatProductInvoice',  'InvoiceItem']

    def setup_main_menu(self, site, profile, m):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('sales.InvoicesToCreate')
