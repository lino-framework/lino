# Copyright 2010-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""Adds functionality for uploading files to the server and managing them.  See
:doc:`/specs/uploads`.


"""
from os.path import join
from lino import ad, _


KB = 2 ** 10

class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."

    verbose_name = _("Uploads")
    menu_group = "office"

    max_file_size = 500 * KB
    """Refuse to upload files that are larger than this (in bytes)."""

    upload_to_tpl = 'uploads/%Y/%m'
    """The value to use as
    `upload_to
    <https://docs.djangoproject.com/en/3.1/ref/models/fields/#django.db.models.FileField.upload_to>`__
    for the :attr:`Upload.file` field.
    """

    remove_orphaned_files = False
    """
    Whether `checkdata --fix` should automatically delete orphaned files in the
    uploads folder.

    """

    def on_ui_init(self, kernel):
        from django.conf import settings
        super(Plugin, self).on_ui_init(kernel)
        kernel.site.makedirs_if_missing(self.get_uploads_root())

    def get_uploads_root(self):
        # from django.conf import settings
        # return join(settings.SITE.MEDIA_ROOT, 'uploads')
        return join(self.site.django_settings['MEDIA_ROOT'], 'uploads')

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
