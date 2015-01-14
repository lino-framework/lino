# Copyright 2013 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Add comments to any model instance.

"""

from lino import ad

from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):
    verbose_name = _("Comments")

    def setup_main_menu(config, site, profile, m):
        system = site.plugins.system
        m = m.add_menu("office", system.OFFICE_MODULE_LABEL)
        m.add_action('comments.MyComments')

    def setup_explorer_menu(config, site, profile, m):
        system = site.plugins.system
        m = m.add_menu("office", system.OFFICE_MODULE_LABEL)
        m.add_action('comments.Comments')
