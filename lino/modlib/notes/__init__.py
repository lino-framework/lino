# Copyright 2013-2015 Luc Saffre
# License: BSD (see file COPYING for details)


"""
Adds a multipurpose model "Note"

.. autosummary::
   :toctree:

   choicelists
   models
   fixtures.demo
   fixtures.std

"""

from lino import ad
from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):

    "See :doc:`/dev/plugins`."

    verbose_name = _("Notes")

    def setup_main_menu(config, site, profile, m):
        mg = site.plugins.office
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('notes.MyNotes')

    def setup_config_menu(config, site, profile, m):
        mg = site.plugins.office
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('notes.NoteTypes')
        m.add_action('notes.EventTypes')

    def setup_explorer_menu(config, site, profile, m):
        mg = site.plugins.office
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('notes.AllNotes')

