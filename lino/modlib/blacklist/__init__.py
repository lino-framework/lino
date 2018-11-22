# -*- coding: UTF-8 -*-
# Copyright 2017 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""I started this plugin just out of curiosity.  When finished it
would do the same as ipdict except that it uses the Django sessions to
store and display these data. Advantage would be that we don't need to
worry what happens when a site has so many http connections that
storing an IPRecord for each of them will cause a memory overflow...


.. autosummary::
   :toctree:

    models

"""

from lino.api import ad


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."

    needs_plugins = ['django.contrib.sessions']

    def setup_site_menu(config, site, user_type, m):
        m.add_action(site.modules.blacklist.Sessions)
