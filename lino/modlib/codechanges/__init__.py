# Copyright 2008-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Adds functionality for managing code changes.

.. autosummary::
   :toctree:

    models

"""

from lino import ad


class Plugin(ad.Plugin):

    def setup_explorer_menu(config, site, profile, m):
        mg = site.plugins.system
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('codechanges.CodeChanges')
