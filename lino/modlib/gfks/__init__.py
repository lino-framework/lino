# Copyright 2008-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""See :doc:`/specs/gfks`.

"""

from lino.api import ad


class Plugin(ad.Plugin):

    """Base class for this plugin."""

    needs_plugins = ['lino.modlib.system', 'django.contrib.contenttypes']

    # def setup_reports_menu(config, site, user_type, m):
    #     hook = site.plugins.system
    #     m = m.add_menu(hook.app_label, hook.verbose_name)
    #     m.add_action(site.modules.gfks.BrokenGFKs)

    def setup_config_menu(config, site, user_type, m):
        hook = site.plugins.system
        m = m.add_menu(hook.app_label, hook.verbose_name)
        m.add_action(site.modules.gfks.HelpTexts)

    def setup_explorer_menu(config, site, user_type, m):
        hook = site.plugins.system
        m = m.add_menu(hook.app_label, hook.verbose_name)
        m.add_action(site.modules.gfks.ContentTypes)



