# Copyright 2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""Adds functionality for instant messageing through websockets.

See :doc:`/specs/chat`.

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

    needs_plugins = ['lino.modlib.notify','lino_xl.lib.groups']
    #extends_models = ['Group']

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
