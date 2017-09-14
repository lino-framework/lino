# Copyright 2014-2017 Luc Saffre
# License: BSD (see file COPYING for details)

"""Defines some system models, especially the :class:`SiteConfig` model.

This plugin is installed in most Lino applications.

.. autosummary::
   :toctree:

   choicelists
   models


"""

from lino import ad
from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."

    verbose_name = _("System")

    needs_plugins = ['lino.modlib.printing']

    def setup_config_menu(self, site, user_type, m):
        system = m.add_menu(self.app_label, self.verbose_name)
        system.add_instance_action(site.site_config)
