from channels.routing import route, include

from .consumers import ws_receive, ws_connect, ws_disconnect, user_connected

# There's no path matching on these routes; we just rely on the matching
# from the top-level routing. We _could_ path match here if we wanted.

websocket_routing = [
    # Called when WebSockets connect
    route("websocket.connect", ws_connect),
    # Called when WebSockets disconnect
    route("websocket.disconnect", ws_disconnect),
    # Called when WebSockets get sent a data frame
    route("websocket.receive", ws_receive),
]

# You can have as many lists here as you like, and choose any name.
# Just refer to the individual names in the include() function.
custom_routing = [
    # Handling different chat commands (websocket.receive is decoded and put
    # onto this channel) - routed on the "command" attribute of the decoded
    # message.
    # route("notify.receive", set_notification_as_seen, command="^seen", ),
    # route("notify.receive", user_connected, command='^/user_connect/'),
    route("websocket.receive", user_connected),
]

channel_routing = [
    # Include sub-routing from an app.
    include(websocket_routing, path=r"^/lino"),

    # Custom handler for message sending (see Room.send_message).
    # Can't go in the include above as it's not got a `path` attribute to match on.
    include(custom_routing),

    # A default "http.request" route is always inserted by Django at the end of the routing list
    # that routes all unmatched HTTP requests to the Django view system. If you want lower-level
    # HTTP handling - e.g. long-polling - you can do it here and route by path, and let the rest
    # fall through to normal views.
]