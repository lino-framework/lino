# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Functionality for writing sales invoices.

It is implemented by :mod:`lino.modlib.sales` (basic functionality) or
:mod:`lino.modlib.auto.sales` (adds common definitions for automatic
generation of invoices).

.. autosummary::
    :toctree:

    models
    fixtures.demo



"""

from lino import ad
from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."

    verbose_name = _("Sales")

    def setup_config_menu(self, site, profile, m):
        m = m.add_menu("sales", self.verbose_name)
        # m.add_action('sales.InvoicingModes')
        m.add_action('sales.ShippingModes')


