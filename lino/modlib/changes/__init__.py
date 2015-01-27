"""
Recording database changes
==========================

See :ref:`lino.tutorial.watch` for an introduction.

"""
from lino import ad, _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."

    verbose_name = _("Boards")

    def setup_explorer_menu(config, site, profile, m):
        menu_group = site.plugins.system
        m = m.add_menu(menu_group.app_label, menu_group.verbose_name)
        m.add_action('changes.Changes')
