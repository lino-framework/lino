# -*- coding: UTF-8 -*-
# Copyright 2013-2017 Luc Saffre
# License: BSD (see file COPYING for details)
"""Database models for `lino.modlib.comments`.

"""
from __future__ import unicode_literals
from builtins import str

import logging
logger = logging.getLogger(__name__)

from django.utils.translation import ugettext_lazy as _
from django.contrib.humanize.templatetags.humanize import naturaltime

from lino.api import dd
from lino.modlib.users.mixins import My
from lino.utils.xmlgen.html import E
from lino.utils.soup import truncate_comment
from lino.core.gfks import gfk2lookup
from .roles import CommentsReader, CommentsUser, CommentsStaff

class CommentTypes(dd.Table):
    """The table with all existing upload types.

    This usually is accessible via the `Configure` menu.
    """
    required_roles = dd.login_required(CommentsStaff)
    model = 'comments.CommentType'
    column_names = "name *"
    order_by = ["name"]

    insert_layout = """
    name
    id
    """

    detail_layout = """
    id name
    comments.CommentsByType
    """


class Comments(dd.Table):
    required_roles = dd.login_required(CommentsUser)
    slave_grid_format = "summary"

    model = 'comments.Comment'

    insert_layout = dd.InsertLayout("""
    reply_to owner owner_type owner_id
    # comment_type
    short_text
    """, window_size=(60, 10), hidden_elements="reply_to owner owner_type owner_id")

    detail_layout = """
    id user created modified 
    reply_to owner owner_type owner_id comment_type
    short_text
    # more_text
    """

    #~ column_names = "id date user type event_type subject * body_html"
    #~ column_names = "id date user event_type type project subject * body"
    #~ hide_columns = "body"
    #~ hidden_columns = frozenset(['body'])
    #~ order_by = ["id"]
    #~ label = _("Notes")

    @classmethod
    def get_comment_header(cls, comment, ar):
        ch = []
        if (comment.modified - comment.created).total_seconds() < 1:
            t = _("Created " + comment.created.strftime('%Y-%m-%d %H:%M'))
        else:
            t = _("Modified " + comment.modified.strftime('%Y-%m-%d %H:%M'))
        ch.append(ar.obj2html(
            comment, naturaltime(comment.created), title=t))
        ch += [" ", _("by"), " ",
               ar.obj2html(comment.user, str(comment.user))]

        sar = cls.insert_action.request_from(ar)
        # print(20170217, sar)
        sar.known_values = dict(
            reply_to=comment, **gfk2lookup(
                comment.__class__.owner, comment.owner))
        if ar.get_user().authenticated:
            btn = sar.ar2button(None, _(" Reply "), icon_name=None)
            # btn.set("style", "padding-left:10px")
            ch += [" [", btn, "]"]

        ch.append(' ')
        ch.append(
            E.a(u"⁜", onclick="toggle_visibility('comment-{}');".format(
                comment.id), title=_("Hide"), href="#")
        )
        return E.tostring(ch)

    @classmethod
    def as_li(cls, self, ar):
        """Return this comment for usage in a list item as a string with HTML
        tags .

        """
        chunks = [truncate_comment(ar.parse_memo(self.short_text))]

        by = _("{0} by {1}").format(
            naturaltime(self.created), str(self.user))

        if (self.modified - self.created).total_seconds() < 1:
            t = _("Created " + self.created.strftime('%Y-%m-%d %H:%M') )
        else:
            t = _("Modified " + self.modified.strftime('%Y-%m-%d %H:%M') )

        chunks += [
            " (", E.tostring(ar.obj2html(self, by, title=t)), ")"
        ]
        if self.more_text:
            chunks.append(" (...)")

        if ar.get_user().authenticated:
            sar = cls.insert_action.request_from(ar)
            # print(20170217, sar)
            sar.known_values = dict(reply_to=self, owner=self.owner)
            if sar.get_permission():
                btn = sar.ar2button(
                    None, _("Reply"), icon_name=None)
                chunks.append(' '+E.tostring(btn))


        html = ''.join(chunks)
        return html
        # return "<li>" + html + "</li>"


class MyComments(My, Comments):
    required_roles = dd.login_required(CommentsUser)
    auto_fit_column_widths = True
    order_by = ["-modified"]
    column_names = "modified short_text owner *"


class CommentsByX(Comments):
    required_roles = dd.login_required(CommentsReader)
    order_by = ["-created"]

class AllComments(Comments):
    required_roles = dd.login_required(CommentsStaff)
    order_by = ["-created"]


USE_ETREE = False

class RecentComments(Comments):
    """Shows the comments for a given database object.

    .. attribute:: slave_summary


    """

    required_roles = dd.login_required(CommentsReader)
    # required_roles = set([CommentsReader])
    column_names = "short_text created user *"
    stay_in_grid = True
    order_by = ["-created"]
    label = "Recent Comments"
    preview_limit = 10

    @classmethod
    def get_slave_summary(cls, obj, ar):
        """The :meth:`summary view <lino.core.actors.Actor.get_slave_summary>`
        for :class:`RecentComments`.

        """
        sar = cls.request_from(
            ar, master_instance=obj, limit=cls.preview_limit)

        # print "20170208", sar.limit
        html = ""
        items = []
        for o in sar.sliced_data_iterator:
            li = cls.as_li(o, ar)
            if o.owner: #Catch for ownerless hackerish comments
                li += _(" On: ") + E.tostring(ar.obj2html(o.owner))
                
            items.append("<li>{}</li>".format(li))
        # html += "<p>" + E.tostring(btn) + "</p>"
        
        if len(items) > 0:
            html += "<div>{0}</div>".format(''.join(items))

        return ar.html_text(html)


class CommentsByType(CommentsByX):
    master_key = 'comment_type'
    column_names = "short_text created user *"

    
class CommentsByRFC(CommentsByX):
    """Shows the comments for a given database object.

    .. attribute:: slave_summary

        
    """
    master_key = 'owner'
    column_names = "short_text created user *"
    stay_in_grid = True
    insert_layout = dd.InsertLayout("""
    reply_to
    # comment_type
    short_text
    """, window_size=(60, 13), hidden_elements="reply_to")


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

        html += "<ul>"
        for c in sar:
            html += "<li>{}<div id={}>{}</div></li>".format(
                self.get_comment_header(c, sar),
                "comment-" + str(c.id),
                ar.parse_memo(c.short_text))

        html += "</ul>"

        return ar.html_text(html)


def comments_by_owner(obj):
    return CommentsByRFC.request(master_instance=obj)
