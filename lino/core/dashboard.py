# -*- coding: UTF-8 -*-
# Copyright 2016-2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""Defines the :class:`DashboardItem` class.

"""

from lino.api import _
from lino.core.permissions import Permittable
from etgen.html import E, tostring


class DashboardItem(Permittable):
    """Base class for all dashboard items.

    .. attribute:: name

        The name used to reference this item in
        :attr:`Widget.item_name`.

    .. attribute:: width

        The width in percent of total available width.

    .. attribute:: min_count

        Hide this item if there are less than min_count rows.

    """

    width = None
    header_level = None
    min_count = None

    def __init__(self, name, header_level=2, min_count=1):
        self.name = name
        self.header_level = header_level
        self.min_count = min_count

    def render(self, ar, **kwargs):
        """Yield a list of html chunks."""
        return []

    def render_request(self, ar, sar, **kwargs):
        """
        Render the given table action
        request. `ar` is the incoming request (the one which displays
        the dashboard), `sar` is the table we want to show (a child of
        `ar`).

        This is a helper function for shared use by :class:`ActorItem`
        and :class:`RequestItem`.
        """
        from lino.core.tables import TableRequest
        from lino.core.requests import ActionRequest
        # T = sar.actor
        # print("20210112 render_request()", sar.actor, sar)
        if self.min_count is not None:
            if sar.get_total_count() < self.min_count:
                # print("20180212 render no rows in ", sar)
                return
        yield '<div class="dashboard-item">'
        if self.header_level is not None:
            buttons = sar.plain_toolbar_buttons()
            buttons.append(sar.open_in_own_window_button())
            elems = []
            for b in buttons:
                elems.append(b)
                elems.append(' ')
            yield tostring(E.h2(str(sar.actor.get_title_base(sar)), ' ', *elems))

        assert sar.renderer is not None
        if isinstance(sar, TableRequest):
            for e in sar.renderer.table2story(sar, **kwargs):
                yield tostring(e)
        elif isinstance(sar, ActionRequest):
            # example : courses.StatusReport in dashboard
            for e in sar.renderer.show_story(ar, sar.actor.get_story(None, ar), **kwargs):
                yield tostring(e)
        else:
            yield "Cannot render {}".format(sar)
        yield '</div>'


    def serialize(self):
        return dict(
            name=self.name,
            header_level=self.header_level
        )

    def __repr__(self):
        return f"{self.__class__.__module__}.{self.__class__.__name__}({self.name},header_level={self.header_level},min_count={self.min_count})"


class ActorItem(DashboardItem):
    """A dashboard item which simply renders a given actor.
    The actor should be a table, other usage is untested.

    Usage examples:
    - :mod:`lino_xl.lib.blogs`
    - :mod:`lino_book.projects.events`

    .. attribute:: header_level

        The header level.

    """
    def __init__(self, actor, **kwargs):
        self.actor = actor
        super(ActorItem, self).__init__(str(actor), **kwargs)

    def get_view_permission(self, user_type):
        return self.actor.default_action.get_view_permission(user_type)
        # rv = self.actor.default_action.get_view_permission(user_type)
        # print("20210112 get_view_permission", self.actor, rv)
        # return rv

    def get_story(self, ar):
        yield self.actor

    def render(self, ar, **kwargs):
        """Render this table to the dashboard.

        - Do nothing if there is no data.

        - If :attr:`header_level` is not None, add a header

        - Render the table itself by calling
          :meth:`lino.core.requests.BaseRequest.show`

        """

        # from lino.core.tables import AbstractTable
        T = self.actor
        # if isinstance(T, AbstractTable):
        sar = T.request(limit=T.preview_limit, parent=ar)
        # sar = ar.spawn(T, limit=T.preview_limit)
        # sar = ar.spawn_request(actor=T, limit=T.preview_limit)

        # print("20210112 render()", ar, sar, ar.get_user(), sar.get_user())
        for i in self.render_request(ar, sar, **kwargs):
            yield i
        # return
        # for e in T.get_story(None, ar):
        #     yield tostring(e)

    def serialize(self):
        d = super(ActorItem, self).serialize()
        d.update(actor=self.actor.actor_id)
        return d


class RequestItem(DashboardItem):
    """
    Experimentally used in `lino_book.projects.events`.
    """
    def __init__(self, sar, **kwargs):
        self.sar = sar
        super(RequestItem, self).__init__(None, **kwargs)

    def get_view_permission(self, user_type):
        return  self.sar.get_permission()
        # rv = self.sar.get_permission()
        # print("20210112 get_view_permission", self.sar, rv)
        # return rv

    def get_story(self, ar):
        yield self.sar

    def render(self, ar, **kwargs):
        for i in self.render_request(ar, self.sar, **kwargs):
            yield i


# class CustomItem(DashboardItem):
#     """Won't work. Not used and not tested."""
#     def __init__(self, name, func, *args, **kwargs):
#         self.func = func
#         self.args = args
#         self.kwargs = kwargs
#         super(CustomItem, self).__init__(name)

#     def render(self, ar):
#         return self.func(ar, *self.args, **self.kwargs)
