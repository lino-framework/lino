# Copyright 2008-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Adds functionality for managing foos.

.. autosummary::
   :toctree:

    models
    fixtures.std
    fixtures.demo

"""

from lino import ad, _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."

    verbose_name = _("Properties")

    def setup_explorer_menu(self, site, profile, m):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('properties.Properties')

    def setup_config_menu(self, site, profile, m):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('properties.PropGroups')
        m.add_action('properties.PropTypes')
        PropGroup = site.modules.properties.PropGroup
        PropsByGroup = site.modules.properties.PropsByGroup
        for pg in PropGroup.objects.all():
            m.add_action(
                PropsByGroup,
                params=dict(master_instance=pg),
                #~ label=pg.name)
                label=unicode(pg))
