# Copyright 2008-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""See :mod:`ml.boards`.

.. autosummary::
   :toctree:

    models
    mixins

"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."

    verbose_name = _("Boards")

    def setup_config_menu(config, site, profile, m):
        menu_host = site.plugins.contacts
        m = m.add_menu(menu_host.app_label, menu_host.verbose_name)
        m.add_action('boards.Boards')

    def setup_explorer_menu(config, site, profile, m):
        menu_host = site.plugins.contacts
        m = m.add_menu(menu_host.app_label, menu_host.verbose_name)
        m.add_action('boards.Members')

