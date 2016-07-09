# Copyright 2012-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Adds functionality for recording database changes into a database
table.  See :ref:`lino.tutorial.watch` for an introduction.

.. autosummary::
   :toctree:

    models

"""
from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."

    verbose_name = _("Changes")

    needs_plugins = [
        'lino.modlib.notify', 'lino.modlib.users', 'lino.modlib.gfks']

    def setup_explorer_menu(config, site, profile, m):
        menu_group = site.plugins.system
        m = m.add_menu(menu_group.app_label, menu_group.verbose_name)
        m.add_action('changes.Changes')
