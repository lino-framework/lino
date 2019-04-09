# Copyright 2013-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""
Lino's comments framework.  See :doc:`/specs/comments`.

"""

from lino import ad, _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."
    verbose_name = _("Comments")

    site_js_snippets = ['comments/comments.js']
    
    needs_plugins = ['lino.modlib.office', 'lino.modlib.gfks']

    # user_must_publish = True
    # """
    # Whether the users are invited to "publish" their comments.
    # """

    def setup_main_menu(self, site, user_type, m):
        mg = site.plugins.office
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('comments.MyComments')
        # if self.user_must_publish:
        #     m.add_action('comments.MyPendingComments')
        m.add_action('comments.RecentComments')
        

    def setup_config_menu(self, site, user_type, m):
        mg = site.plugins.office
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('comments.CommentTypes')

    def setup_explorer_menu(self, site, user_type, m):
        mg = site.plugins.office
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('comments.AllComments')

    def get_dashboard_items(self, user):
        # if self.user_must_publish:
        #     yield self.site.models.comments.MyPendingComments
        yield self.site.models.comments.RecentComments
