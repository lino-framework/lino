# Copyright 2013-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Add comments to any model instance.

.. autosummary::
   :toctree:

    models


"""

from lino import ad

from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."
    verbose_name = _("Comments")

    needs_plugins = ['lino.modlib.office']

    def setup_main_menu(config, site, profile, m):
        mg = site.plugins.office
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('comments.MyComments')

    def setup_explorer_menu(config, site, profile, m):
        mg = site.plugins.office
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('comments.Comments')
