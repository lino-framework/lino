# Copyright 2008-2016 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""Extends `django.contrib.contenttypes`.  This module must be
installed if your models contain GenericForeignKey fields or inherit
from the :class:`Controllable
<lino.modlib.gfks.mixins.Controllable>` mixin.

.. autosummary::
   :toctree:

    models
    mixins
    fields

"""

from lino.api import ad


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."

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



