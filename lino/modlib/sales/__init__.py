# Copyright 2014 Luc Saffre
# License: BSD (see file COPYING for details)

from lino import ad
from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):

    verbose_name = _("Sales")

    def setup_config_menu(self, site, profile, m):
        m = m.add_menu("sales", self.verbose_name)
        # m.add_action('sales.InvoicingModes')
        m.add_action('sales.ShippingModes')


