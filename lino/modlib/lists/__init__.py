# Copyright 2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Adds the concept of partner lists.
"""

from lino import ad

from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):
    "Ceci n'est pas une documentation."
    verbose_name = _("Lists")

    def setup_main_menu(config, site, profile, m):
        mg = site.plugins.contacts
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('lists.Lists')

    def setup_config_menu(config, site, profile, m):
        mg = site.plugins.contacts
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('lists.ListTypes')

    def setup_explorer_menu(config, site, profile, m):
        mg = site.plugins.contacts
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('lists.Members')
