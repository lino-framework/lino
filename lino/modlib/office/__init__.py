# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Adds a user group "Office" and serves as menu hook for several
other modules.

.. autosummary::

"""

from lino import ad
from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."

    verbose_name = _("Office")

    def on_site_startup(self, site):
        from lino.modlib.users.utils import add_user_group
        add_user_group(self.app_label, self.verbose_name)

    def setup_config_menu(self, site, profile, m):
        if site.user_model is not None:
            p = m.add_menu(self.app_label, self.verbose_name)
            p.add_action('system.MyTextFieldTemplates')

    def setup_explorer_menu(self, site, profile, m):
        if site.user_model is not None:
            p = m.add_menu(self.app_label, self.verbose_name)
            p.add_action('system.TextFieldTemplates')


