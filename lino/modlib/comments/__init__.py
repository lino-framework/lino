# Copyright 2013-2019 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""
Lino's comments framework.  See :doc:`/specs/comments`.

"""

from lino import ad, _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."
    verbose_name = _("Comments")

    site_js_snippets = ['comments/comments.js']

    needs_plugins = ['lino.modlib.office', 'lino.modlib.memo']

    # emotion_range = "social"
    emotion_range = "business"
    """Which range of emotion icons to provide. Either "business" or "social".
    """

    private_default = True
    """Whether comments are private by default.

    The default value for the :attr:`lino.modlib.comments.Comment.private`
    field.

    """

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
        m.add_action('comments.Mentions')
        m.add_action('comments.Reactions')

    def get_dashboard_items(self, user):
        # if self.user_must_publish:
        #     yield self.site.models.comments.MyPendingComments
        yield self.site.models.comments.RecentComments
