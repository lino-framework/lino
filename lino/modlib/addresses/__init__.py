# Copyright 2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""This adds multiple addresses per Partner.

"""

from lino import ad

from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."
    verbose_name = _("Addresses")

    def setup_explorer_menu(self, site, profile, m):
        # mg = self.get_menu_group()
        mg = site.plugins.contacts
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('addresses.AddressTypes')
        m.add_action('addresses.Addresses')

