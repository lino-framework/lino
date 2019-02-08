# Copyright 2010-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""Adds functionality for uploading files to the server and managing them.  See
:doc:`/specs/uploads`.


"""
from lino import ad, _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."

    verbose_name = _("Uploads")
    menu_group = "office"

    def setup_main_menu(self, site, user_type, m):
        mg = self.get_menu_group()
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('uploads.MyUploads')

    def setup_config_menu(self, site, user_type, m):
        mg = self.get_menu_group()
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('uploads.Volumes')
        m.add_action('uploads.UploadTypes')

    def setup_explorer_menu(self, site, user_type, m):
        mg = self.get_menu_group()
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('uploads.AllUploads')
        m.add_action('uploads.UploadAreas')

