# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Defines some system models, especially the :class:`SiteConfig` model.

This app should usually be installed in every Lino application.
But there are exceptions, e.g. :ref:`lino.tutorial.polls`
or :doc:`/tutorials/de_BE/index` don't.

.. autosummary::
   :toctree:

   models
   mixins
   tests


"""

from lino import ad
from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."

    verbose_name = _("System")

    OFFICE_MODULE_LABEL = _("Office")  # TODO: add `lino.modlib.office`

    def setup_config_menu(self, site, profile, m):
        office = m.add_menu("office", self.OFFICE_MODULE_LABEL)
        system = m.add_menu(self.app_label, self.verbose_name)
        system.add_instance_action(site.site_config)
        if site.user_model and profile.authenticated:
            system.add_action(site.user_model)
            office.add_action('system.MyTextFieldTemplates')

    def setup_explorer_menu(self, site, profile, m):
        office = m.add_menu("office", self.OFFICE_MODULE_LABEL)
        system = m.add_menu(self.app_label, self.verbose_name)

        if site.user_model:
            system.add_action(site.modules.users.Authorities)
            system.add_action('system.UserGroups')
            system.add_action('system.UserLevels')
            system.add_action('system.UserProfiles')
            office.add_action('system.TextFieldTemplates')


