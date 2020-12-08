# Copyright 2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""Adds functionality for instant messaging through websockets.

This plugin is a proof of concept with surprising results, but it is in standby
mode now.  It is underdocumented and not covered by any tests. We have abandoned
our dream of writing an instant messenger client in Lino. We rather hope that
sooner or later some free IM client will emerge, and that Lino would rather
integrate with it than replace it.


"""

from lino.api import ad, _
from lino.core.utils import is_devserver
try:
    import redis
except ImportError:
    redis = None
try:
    import channels
except ImportError:
    channels = None


class Plugin(ad.Plugin):
    "See :class:`lino.core.plugin.Plugin`."

    verbose_name = _("Chat")

    needs_plugins = ['lino.modlib.notify', 'lino_xl.lib.groups']

    media_name = 'js'

    def on_init(self):
        if not self.site.use_websockets:
            raise Warning("Chat requires use_websockets = True")

    # def get_requirements(self, site):
    #     # handled by modlib.notify
    #     pass

    # def get_used_libs(self, html=None):
    #     handled by modlib.notify
        # pass


    def setup_main_menu(self, site, user_type, m):
    #     todo,
        # pass

        p = site.plugins.office
        m = m.add_menu(p.app_label, p.verbose_name)
        m.add_action('chat.ChatMessages')

    def setup_explorer_menu(self, site, user_type, m):
        # todo,
        #pass
        p = site.plugins.system
        m = m.add_menu(p.app_label, p.verbose_name)
        m.add_action('chat.ChatMessages')
        m.add_action('chat.ChatGroups')


    def get_head_lines(self, site, request):
        """Adds a JS constant to let react know we want to include WS chat info"""
        if not self.site.use_websockets:
            yield ""
        # from lino.utils.jsgen import py2js
        else :
            yield """
        <script type="text/javascript">
            window.Lino = window.Lino || {}
            window.Lino.useChats = true;
        </script>
            """

    # def get_dashboard_items(self, user):
    #     if user.authenticated:
            # yield ActorItem(
            #     self.models.notify.MyMessages, header_level=None)
            # yield self.site.models.notify.MyMessages
