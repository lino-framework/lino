# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Adds functionality and models to handle multiple addresses per
:class:`lino.modlib.contacts.models.Partner`. When this module is
installed, your application usually has a "Manage addresses" button
per partner.

.. autosummary::
   :toctree:

    choicelists
    mixins
    models
    fixtures.demo2

Some unit test cases are :mod:`lino.projects.min2.tests.test_addresses`.

"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."
    verbose_name = _("Addresses")

    def setup_explorer_menu(self, site, profile, m):
        # mg = self.get_menu_group()
        mg = site.plugins.contacts
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('addresses.AddressTypes')
        m.add_action('addresses.Addresses')

