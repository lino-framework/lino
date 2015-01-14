# Copyright 2010-2011 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Defines an Upload model.

"""
from lino import ad
from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):

    verbose_name = _("Uploads")

    def setup_main_menu(config, site, profile, m):
        system = site.plugins.system
        m = m.add_menu("office", system.OFFICE_MODULE_LABEL)
        m.add_action('uploads.MyUploads')

    def setup_config_menu(config, site, profile, m):
        system = site.plugins.system
        m = m.add_menu("office", system.OFFICE_MODULE_LABEL)
        m.add_action('uploads.UploadTypes')

    def setup_explorer_menu(config, site, profile, m):
        system = site.plugins.system
        m = m.add_menu("office", system.OFFICE_MODULE_LABEL)
        m.add_action('uploads.Uploads')
        m.add_action('uploads.UploadAreas')
