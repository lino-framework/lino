# Copyright 2008-2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""Adds functionality for managing notification messages.

See :doc:`/specs/notify`.

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

    verbose_name = _("Messages")

    needs_plugins = ['lino.modlib.users', 'lino.modlib.memo']

    remove_after = 24
    """Automatically remove notification messages after x hours.

    Set this to None or 0 to deactivate cleanup and keep messages
    forever.

    """

    keep_unseen = True
    """Whether to keep unseen messages when removing old messages
    according to :attr:`remove_after`.

    In normal operation this should be True, but e.g. after a flood
    of messages during experimental phases we might want to get rid of
    them automatically.

    """

    media_name = 'js'

    # email_subject_template = "Message about {obj.owner}"
    # """The template used to build the subject lino of message emails.

    # :obj: is the :class:`Message
    #       <lino.modlib.notify.models.Message>` object.

    # """

    def on_init(self):
        if self.site.use_websockets:
            if channels is None:
                # if channels is not installed, we cannot use it as a plugin
                # because even :manage:`install` would fail.
                return
            self.needs_plugins.append('channels')

            sd = self.site.django_settings
            # the dict which will be used to create settings
            cld = {}
            sd['CHANNEL_LAYERS'] = {"default": cld}
            #if not DJANGO2:
            #    cld["ROUTING"] = "lino.modlib.notify.routing.channel_routing"
            #    cld["BACKEND"] = "asgiref.inmemory.ChannelLayer"
            #else:
            sd['ASGI_APPLICATION'] = "lino.modlib.notify.routing2.application"
            cld["BACKEND"] = "channels_redis.core.RedisChannelLayer"
            cld['CONFIG'] = {"hosts": [("localhost", 6379)], }
            if False:  # not is_devserver():
                cld['BACKEND'] = "asgi_redis.RedisChannelLayer"
                cld['CONFIG'] = {"hosts": [("localhost", 6379)], }

    def get_requirements(self, site):
        if site.use_websockets:
            yield 'channels'
            # yield 'asgiref'
            yield 'channels_redis'
            if False:  # not is_devserver():
                yield 'asgi_redis'

    def get_used_libs(self, html=None):
        try:
            import channels
            version = channels.__version__
        except ImportError:
            version = self.site.not_found_msg
        name = "Channels ({})".format(
            "active" if self.site.use_websockets else "inactive")

        yield (name, version, "https://github.com/django/channels")

    def get_js_includes(self, settings, language):
        if self.site.use_websockets:
            if settings.DEBUG:
                yield self.build_lib_url(('push.js/push.min.js'))
            else:
                yield self.build_lib_url(('push.js/push.js'))

    def setup_main_menu(self, site, user_type, m):
        p = site.plugins.office
        m = m.add_menu(p.app_label, p.verbose_name)
        m.add_action('notify.MyMessages')

    def setup_explorer_menu(self, site, user_type, m):
        p = site.plugins.system
        m = m.add_menu(p.app_label, p.verbose_name)
        m.add_action('notify.AllMessages')

    def get_head_lines(self, site, request):
        if not self.site.use_websockets:
            return
        from lino.utils.jsgen import py2js
        user_name = "anony"
        if request.user.is_authenticated:
            user_name = request.user.username
        site_title = site.title or 'Lino-framework'
        if self.site.default_ui == 'lino_react.react':
            js_to_add = """
        <script type="text/javascript">
            window.Lino = window.Lino || {}
            window.Lino.useWebSockets = true;
        </script>
            """
        else:
            js_to_add = ("""
        <script type="text/javascript">
        Ext.onReady(function() {
            // Note that the path doesn't matter for routing; any WebSocket
            // connection gets bumped over to WebSocket consumers
            var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
            var ws_path = window.location.pathname + "lino/";
            console.log("Connecting to " + ws_path);
            var webSocketBridge = new channels.WebSocketBridge();
            var username = '%s' ;
            webSocketBridge.connect();
            lino_connecting = function() {
                console.log("lino connecting ...");
                webSocketBridge.send({
                            "command": "user_connect",
                            "username": username
                        });
            }
            webSocketBridge.socket.addEventListener('open', function() {
                lino_connecting();
            });
            // Helpful debugging
            webSocketBridge.socket.onclose = function () {
                console.log("Disconnected from chat socket");
            }

            onGranted = console.log("onGranted");
            onDenied = console.log("onDenied");
            // Ask for permission if it's not already granted
            Push.Permission.request(onGranted,onDenied);

            webSocketBridge.listen(function(action, stream) {
                try {
                    Push.create( %s , {
                        body: action['body'],
                        icon: '/static/img/lino-logo.png',
                        onClick: function () {
                            window.focus();
                            """ + site.kernel.default_renderer.reload_js() + """
                            this.close();
                        }
                    });
                    if (false && Number.isInteger(action["id"])){
                        webSocketBridge.stream('lino').send({message_id: action["id"]})
                        webSocketBridge.send(JSON.stringify({
                                        "command": "seen",
                                        "message_id": action["id"],
                                    }));
                                }
                    }
                catch(err) {
                    console.log(err.message);
                }
            })});
        // end of onReady()"
        </script>
            """) % (user_name, py2js(site_title))
        yield js_to_add

    def get_dashboard_items(self, user):
        if user.is_authenticated:
            # yield ActorItem(
            #     self.models.notify.MyMessages, header_level=None)
            yield self.site.models.notify.MyMessages
