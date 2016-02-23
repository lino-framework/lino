# Copyright 2014-2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""Defines some system models, especially the :class:`SiteConfig` model.

This app should usually be installed in every Lino application.
But there are exceptions, e.g. :ref:`lino.tutorial.polls`
or :doc:`/tutorials/de_BE/index` don't.

.. autosummary::
   :toctree:

   choicelists
   mixins
   models
   tests


"""

from lino import ad
from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."

    verbose_name = _("System")

    needs_plugins = ['lino.modlib.printing']

    def setup_config_menu(self, site, profile, m):
        system = m.add_menu(self.app_label, self.verbose_name)
        system.add_instance_action(site.site_config)
