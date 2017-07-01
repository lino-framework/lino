# Copyright 2013-2017 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Add comments to any model instance.

.. autosummary::
   :toctree:

    models
    mixins
    fixtures.demo2

"""

from lino import ad

from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."
    verbose_name = _("Comments")

    site_js_snippets = ['comments/comments.js']
    
    needs_plugins = ['lino.modlib.office']

    # commentable_model = None

    # def on_site_startup(self, site):
    #     if self.commentable_model is not None:
    #         self.commentable_model = site.models.resolve(
    #             self.commentable_model)
    #     super(Plugin, self).on_site_startup(site)
    

    def setup_main_menu(config, site, user_type, m):
        mg = site.plugins.office
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('comments.MyComments')

    def setup_config_menu(config, site, user_type, m):
        mg = site.plugins.office
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('comments.CommentTypes')

    def setup_explorer_menu(config, site, user_type, m):
        mg = site.plugins.office
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('comments.AllComments')

    def unused_get_dashboard_items(self, user):
        # removed because it is rather disturbing to see all comments
        yield self.site.models.comments.RecentComments
