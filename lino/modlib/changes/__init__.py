# Copyright 2012-2017 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""Adds functionality for recording database changes into a database
table.  See :ref:`dev.watch` for an introduction.

.. autosummary::
   :toctree:

    models

"""
from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."

    verbose_name = _("Changes")

    needs_plugins = [
        'lino.modlib.users', 'lino.modlib.gfks']

    def setup_explorer_menu(config, site, user_type, m):
        menu_group = site.plugins.system
        m = m.add_menu(menu_group.app_label, menu_group.verbose_name)
        m.add_action('changes.Changes')
