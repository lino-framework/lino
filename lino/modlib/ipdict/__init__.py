# -*- coding: UTF-8 -*-
# Copyright 2017 Luc Saffre
# License: BSD (see file COPYING for details)

"""The models module for this plugin.

.. autosummary::
   :toctree:

    models
    middleware

"""

from lino.api import ad


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."

    def setup_site_menu(config, site, profile, m):
        m.add_action(site.modules.ipdict.Connections)
