# -*- coding: UTF-8 -*-
# Copyright 2013-2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""Database models for `lino.modlib.comments`.

"""

import logging
logger = logging.getLogger(__name__)

try:
    import bleach
except ImportError:
    bleach = None

from django.utils.translation import ugettext_lazy as _
from django.contrib.humanize.templatetags.humanize import naturaltime

from lino.api import dd
from lino.modlib.users.mixins import ByUser
from lino.utils.xmlgen.html import E


class Comments(dd.Table):
    required_roles = dd.required(dd.SiteStaff)
    slave_grid_format = "summary"

    model = 'comments.Comment'

    insert_layout = dd.FormLayout("""
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


class MyComments(ByUser, Comments):
    required_roles = dd.required()
    auto_fit_column_widths = True
    order_by = ["modified"]
    column_names = "modified short_text owner *"


class CommentsByX(Comments):
    required_roles = dd.required()
    order_by = ["-created"]

USE_ETREE = False


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

        items = [o.as_li(ar) for o in sar]
        if len(items) > 0:
            html += u"<ul>{0}</ul>".format(''.join(items))

        return u"""<div class="htmlText">{0}</div>""".format(html)
        # return html


def comments_by_owner(obj):
    return CommentsByRFC.request(master_instance=obj)
