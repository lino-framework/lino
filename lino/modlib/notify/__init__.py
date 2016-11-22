# Copyright 2008-2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""Adds functionality for managing messages.

.. autosummary::
   :toctree:

    models
    actions
    mixins
    utils
    fixtures.demo2

Templates used by this plugin
=============================

.. xfile:: notify/body.eml

    A Jinja template used for generating the body of the email when
    sending a message per email to its recipient.

    Available context variables:

    - ``obj`` -- The :class:`Message
      <lino.modlib.notify.models.Message>` instance being sent.

    - ``E`` -- The html namespace :mod:`lino.utils.xmlgen.html`

    - ``rt`` -- The runtime API :mod:`lino.api.rt`

    - ``ar`` -- The action request which caused the message. a
      :class:`BaseRequest <lino.core.requests.BaseRequest>` instance.

"""

from lino.api import ad, _
# from django.conf import settings

try:
    import redis
except:
    redis = False


class Plugin(ad.Plugin):
    "See :class:`lino.core.plugin.Plugin`."

    use_websockets = True
    """Set this to False in order to deactivate use of websockets and
    channels.

    """

    verbose_name = _("Messages")

    needs_plugins = ['lino.modlib.users', 'lino.modlib.gfks']
    if use_websockets:
        needs_plugins.append('channels')

    media_name = 'js'

    # email_subject_template = "Message about {obj.owner}"
    # """The template used to build the subject lino of message emails.

    # :obj: is the :class:`Message
    #       <lino.modlib.notify.models.Message>` object.

    # """

    def on_init(self):
        if self.use_websockets:
            sd = self.site.django_settings  # the dict which will be
                                            # used to create settings
            sd['CHANNEL_LAYERS'] = {
                "default": {
                    "BACKEND": "asgiref.inmemory.ChannelLayer",
                    "ROUTING": "lino.modlib.notify.routing.channel_routing",
                },
            }
            if redis:
                rs = redis.Redis("localhost")
                try:
                    response = rs.client_list()
                    sd['CHANNEL_LAYERS']['default']['BACKEND'] = "asgi_redis.RedisChannelLayer"
                    sd['CHANNEL_LAYERS']['default']['CONFIG'] = {"hosts": [("localhost", 6379)], }
                except redis.ConnectionError:
                    pass

    def get_js_includes(self, settings, language):
        if self.use_websockets:
            yield self.build_lib_url('reconnecting-websocket/reconnecting-websocket.min.js')
            if settings.DEBUG:
                yield self.build_lib_url(('push.js/push.min.js'))
            else:
                yield self.build_lib_url(('push.js/push.js'))

    def setup_main_menu(self, site, profile, m):
        p = site.plugins.office
        m = m.add_menu(p.app_label, p.verbose_name)
        m.add_action('notify.MyMessages')

    def setup_explorer_menu(self, site, profile, m):
        p = site.plugins.system
        m = m.add_menu(p.app_label, p.verbose_name)
        m.add_action('notify.AllMessages')

    def get_head_lines(self, site, request):
        from lino.utils.jsgen import py2js
        if not self.use_websockets:
            return
        user_name = "anony"
        if request.user.authenticated:
            user_name = request.user.username
        site_title = site.title

        js_to_add = """
    <script type="text/javascript">
    Ext.onReady(function() {
        // Note that the path doesn't matter for routing; any WebSocket
        // connection gets bumped over to WebSocket consumers
        var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
        var ws_path = ws_scheme + '://' + window.location.host + "/websocket/";
        console.log("Connecting to " + ws_path);
        var socket = new ReconnectingWebSocket(ws_path);

        onGranted = console.log("onGranted");
        onDenied = console.log("onDenied");
        // Ask for permission if it's not already granted
        Push.Permission.request(onGranted,onDenied);
        socket.onmessage = function(e) {
            try {
                var json_data = JSON.parse(e.data);
                Push.create( %s , {
                    body: json_data['body'],
                    icon: '/static/img/lino-logo.png',
                    onClick: function () {
                        window.focus();
                        Lino.viewport.refresh();
                        this.close();
                    }
                });
                if (false && Number.isInteger(JSON.parse(e.data)["id"])){
                    socket.send(JSON.stringify({
                                    "command": "seen",
                                    "message_id": JSON.parse(e.data)["id"],
                                }));
                            }
                }
            catch(err) {
                console.log(err.message);
            }
        }
        // Call onopen directly if socket is already open
        if (socket.readyState == WebSocket.OPEN) socket.onopen();
        else {
        socket.onopen = function() {
            socket.send(JSON.stringify({
                            "command": "user_connect",
                            "username": "%s",
                        }));
        }
        }
    }); // end of onReady()"
    </script>
        """ % (py2js(site_title), user_name)
        yield js_to_add
