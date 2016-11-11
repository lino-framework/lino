# Copyright 2008-2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""Adds functionality for managing notifications.

.. autosummary::
   :toctree:

    models
    actions
    mixins
    utils

Templates used by this plugin
=============================

.. xfile:: notify/body.eml

    A Jinja template used for generating the body of the email when
    sending a notification per email to its recipient.

    Available context variables:

    - ``obj`` -- The :class:`Notification
      <lino.modlib.notify.models.Notification>` instance being sent.

    - ``E`` -- The html namespace :mod:`lino.utils.xmlgen.html`

    - ``rt`` -- The runtime API :mod:`lino.api.rt`

    - ``ar`` -- The action request which caused the notification. a
      :class:`BaseRequest <lino.core.requests.BaseRequest>` instance.

"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :class:`lino.core.plugin.Plugin`."

    use_websockets = True
    """Set this to False in order to deactivate use of websockets and
    channels.

    """

    verbose_name = _("Notifications")

    needs_plugins = ['lino.modlib.users', 'lino.modlib.gfks']
    if use_websockets:
        needs_plugins.append('channels')

    media_name = 'js'

    # email_subject_template = "Notification about {obj.owner}"
    # """The template used to build the subject lino of notification emails.

    # :obj: is the :class:`Notification
    #       <lino.modlib.notify.models.Notification>` object.

    # """

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
        m.add_action('notify.MyNotifications')

    def setup_explorer_menu(self, site, profile, m):
        p = site.plugins.system
        m = m.add_menu(p.app_label, p.verbose_name)
        m.add_action('notify.AllNotifications')

    def get_head_lines(self, site, request):
        if not self.use_websockets:
            return
        user_name = "anony"
        if request.user.authenticated:
            user_name = request.user.username

        site_title = site.verbose_name

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
        var site_title = "%s" ;
        socket.onmessage = function(e) {
            try {
                var json_data = JSON.parse(e.data);
                Push.create(site_title, {
                    body: json_data['body'],
                    icon: 'img/lino-logo.png',
                    onClick: function () {
                        window.focus();
                        this.close();
                    }
                });
                if ( Number.isInteger(JSON.parse(e.data)["id"])){
                    socket.send(JSON.stringify({
                                    "command": "seen",
                                    "notification_id": JSON.parse(e.data)["id"],
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
        """ % (site_title, user_name)
        yield js_to_add
