# Copyright 2008-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Adds functionality for "starring" database objects (marking them as
"favourite").

.. autosummary::
   :toctree:

    models

"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :class:`lino.core.plugin.Plugin`."

    verbose_name = _("Stars")

    needs_plugins = ['lino.modlib.changes', 'lino.modlib.office']

    def setup_main_menu(self, site, profile, m):
        # p = self.get_menu_group()
        p = self.site.plugins.office
        m = m.add_menu(p.app_label, p.verbose_name)
        m.add_action('stars.MyStars')

    def setup_explorer_menu(self, site, profile, m):
        # p = self.get_menu_group()
        p = self.site.plugins.office
        m = m.add_menu(p.app_label, p.verbose_name)
        m.add_action('stars.Stars')
