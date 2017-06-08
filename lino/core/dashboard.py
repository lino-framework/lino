# -*- coding: UTF-8 -*-
# Copyright 2016-2017 Luc Saffre.
# License: BSD, see LICENSE for more details.
"""Defines the :class:`DashboardItem` class.

"""
from __future__ import unicode_literals


from lino.api import _
from lino.core.permissions import Permittable
from lino.utils.xmlgen.html import E

class DashboardItem(Permittable):
    """Base class for all dashboard items.

    .. attribute:: name

        The name used to reference this item in
        :attr:`Widget.item_name`.

    .. attribute:: width

        The width in percent of total available width.

    """

    width = None
    
    def __init__(self, name):
        self.name = name
        
    def render(self, ar):
        """Return a HTML string """

class ActorItem(DashboardItem):
    """The only one that's being used.

    See :mod:`lino_xl.lib.blogs` as a usage example.

    .. attribute:: header_level

        The header level.

    """
    def __init__(self, actor, header_level=2):
        self.actor = actor
        self.header_level = header_level
        super(ActorItem, self).__init__(str(actor))
        
    def get_view_permission(self, user_type):
        return self.actor.default_action.get_view_permission(user_type)

    def render(self, ar):
        """Render this table to the dashboard.

        - Do nothing if there is no data.

        - If :attr:`header_level` is not None, add a header

        - Render the table itself by calling
          :meth:`lino.core.requests.BaseRequest.show`

        """
        T = self.actor
        sar = ar.spawn(T, limit=T.preview_limit)
        if not sar.get_total_count():
            return ''
        if self.header_level is None:
            s = ''
        else:
            s = E.tostring(E.h2(
                T.label, ' ', ar.window_action_button(
                    T.default_action,
                    # label="🗗",
                    # label="☌",  # conjunction
                    # label="◱", # 25F1
                    # label="◳", # 25F3
                    # label="⏍", # 23CD
                    label="⍐", # 2350
                    # style="text-decoration:none; font-size:80%;",
                    style="text-decoration:none;",
                    title=_("Show this table in own window"))))

        s += E.tostring(ar.show(sar))
        return s
            

class CustomItem(DashboardItem):
    """Won't work. Not used and not tested."""
    def __init__(self, name, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        super(CustomItem, self).__init__(name)
        
    def render(self, ar):
        return self.func(ar, *self.args, **self.kwargs)
                          
