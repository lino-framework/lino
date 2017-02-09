# -*- coding: UTF-8 -*-
# Copyright 2013-2017 Luc Saffre
# License: BSD (see file COPYING for details)
"""Database models for `lino.modlib.comments`.

"""
from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

from django.utils.translation import ugettext_lazy as _
from django.contrib.humanize.templatetags.humanize import naturaltime

from lino.api import dd
from lino.modlib.users.mixins import My
from lino.modlib.office.roles import OfficeStaff, OfficeUser
from lino.utils.xmlgen.html import E


class Comments(dd.Table):
    required_roles = dd.required(OfficeStaff)
    slave_grid_format = "summary"

    model = 'comments.Comment'

    insert_layout = dd.InsertLayout("""
    short_text
    """, window_size=(40, 10))

    detail_layout = """
    id user created modified owner
    short_text
    more_text
    """

    #~ column_names = "id date user type event_type subject * body_html"
    #~ column_names = "id date user event_type type project subject * body"
    #~ hide_columns = "body"
    #~ hidden_columns = frozenset(['body'])
    #~ order_by = ["id"]
    #~ label = _("Notes")


class MyComments(My, Comments):
    required_roles = dd.required(OfficeUser)
    auto_fit_column_widths = True
    order_by = ["modified"]
    column_names = "modified short_text owner *"


class CommentsByX(Comments):
    required_roles = dd.required(OfficeUser)
    order_by = ["-created"]

USE_ETREE = False


class RecentComments(Comments):
    """Shows the comments for a given database object.

    .. attribute:: slave_summary


    """

    required_roles = set([])
    column_names = "short_text created user *"
    stay_in_grid = True
    order_by = ["-created"]
    label = "Recent Comments"

    @classmethod
    def get_slave_summary(self, obj, ar):
        """The :meth:`summary view <lino.core.actors.Actor.get_slave_summary>`
        for :class:`RecentComments`.

        """
        sar = self.request_from(ar, master_instance=obj)

        # print "20170208", sar, obj, sar
        html = ""
        items = []
        for o in sar:
            li = o.as_li(ar)
            if o.owner: #Catch for ownerless hackerish comments
                li += _(" On: ") + E.tostring(ar.obj2html(o.owner))
                
            items.append("<li>{}</li>".format(li))
        # html += "<p>" + E.tostring(btn) + "</p>"
        
        if len(items) > 0:
            html += "<div>{0}</div>".format(''.join(items))

        return ar.html_text(html)


class CommentsByRFC(CommentsByX):
    """Shows the comments for a given database object.

    .. attribute:: slave_summary

        
    """
    master_key = 'owner'
    column_names = "short_text created user *"
    stay_in_grid = True

    @classmethod
    def get_slave_summary(self, obj, ar):
        """The :meth:`summary view <lino.core.actors.Actor.get_slave_summary>`
        for :class:`CommentsByRFC`.

        """
        sar = self.request_from(ar, master_instance=obj)

        html = obj.get_rfc_description(ar)
        sar = self.insert_action.request_from(sar)
        if sar.get_permission():
            btn = sar.ar2button(None, _("Write comment"), icon_name=None)
            html += "<p>" + E.tostring(btn) + "</p>"

        items = ["<li>{}</li>".format(o.as_li(ar)) for o in sar]
        if len(items) > 0:
            html += u"<ul>{0}</ul>".format(''.join(items))

        return ar.html_text(html)


def comments_by_owner(obj):
    return CommentsByRFC.request(master_instance=obj)
