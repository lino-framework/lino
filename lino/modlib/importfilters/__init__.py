# Copyright 2008-2015 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""
Import filters
"""

from lino import ad

from django.utils.translation import gettext_lazy as _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."
    verbose_name = _("Import filters")

    def setup_config_menu(config, site, user_type, m):
        p = site.plugins.importfilters
        m = m.add_menu('filters', p.verbose_name)
        m.add_action('importfilters.Filters')
        m.add_action('importfilters.Import')

    def setup_explorer_menu(config, site, user_type, m):
        p = site.plugins.importfilters
        m = m.add_menu('filters', p.verbose_name)
        m.add_action('importfilters.Filters')
