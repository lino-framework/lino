# Copyright 2008-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Not used. Adds functionality for managing families.

.. autosummary::
   :toctree:

    models

"""

from lino import ad, _


class Plugin(ad.Plugin):

    "See :doc:`/dev/plugins`."

    verbose_name = _("Families")

    def setup_explorer_menu(config, site, profile, m):
        mg = site.plugins.contacts
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('families.Couples')
