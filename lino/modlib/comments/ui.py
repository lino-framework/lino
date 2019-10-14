# -*- coding: UTF-8 -*-
# Copyright 2013-2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
from __future__ import unicode_literals
from builtins import str

from django.utils.translation import ugettext_lazy as _
from django.contrib.humanize.templatetags.humanize import naturaltime

from lino.api import dd
from lino.modlib.users.mixins import My
from etgen.html import E, tostring
# from lxml import etree
import lxml
# from lino.utils.soup import truncate_comment
from lino.core.gfks import gfk2lookup
from .roles import CommentsReader, CommentsUser, CommentsStaff
from .choicelists import CommentEvents


class CommentTypes(dd.Table):
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

    model = 'comments.Comment'
    params_layout = "start_date end_date observed_event user"

    insert_layout = dd.InsertLayout("""
    reply_to owner owner_type owner_id
    # comment_type
    body
    """, window_size=(60, 10), hidden_elements="reply_to owner owner_type owner_id")

    detail_layout = """
    id user created modified
    reply_to owner owner_type owner_id comment_type
    body
    """

    # html_parser = etree.HTMLParser()

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
                comment.id), title=str(_("Hide")), href="#")
        )
        return tostring(ch)

    @classmethod
    def as_li(cls, self, ar):
        # chunks = [ar.parse_memo(self.short_preview)]
        chunks = [self.short_preview]

        by = _("{0} by {1}").format(
            naturaltime(self.created), str(self.user))

        if (self.modified - self.created).total_seconds() < 1:
            t = _("Created " + self.created.strftime('%Y-%m-%d %H:%M') )
        else:
            t = _("Modified " + self.modified.strftime('%Y-%m-%d %H:%M') )

        chunks += [
            " (", tostring(ar.obj2html(self, by, title=t)), ")"
        ]
        # if self.more_text:
        #     chunks.append(" (...)")

        if ar.get_user().authenticated:
            sar = cls.insert_action.request_from(ar)
            # print(20170217, sar)
            sar.known_values = dict(reply_to=self, owner=self.owner)
            if sar.get_permission():
                btn = sar.ar2button(
                    None, _("Reply"), icon_name=None)
                chunks.append(' '+tostring(btn))


        html = ''.join(chunks)
        return html
        # return "<li>" + html + "</li>"


class MyComments(My, Comments):
    required_roles = dd.login_required(CommentsUser)
    auto_fit_column_widths = True
    order_by = ["-modified"]
    column_names = "id modified short_preview owner workflow_buttons *"


class AllComments(Comments):
    required_roles = dd.login_required(CommentsStaff)
    order_by = ["-created"]

class CommentsByX(Comments):
    required_roles = dd.login_required(CommentsReader)
    order_by = ["-created"]
    display_mode = "summary"


# class MyPendingComments(MyComments):
#     label = _("My pending comments")
#     welcome_message_when_count = 0

#     @classmethod
#     def param_defaults(cls, ar, **kw):
#         kw = super(MyPendingComments, cls).param_defaults(ar, **kw)
#         kw.update(show_published=dd.YesNo.no)
#         return kw

class RecentComments(Comments):
    required_roles = dd.login_required(CommentsReader)
    # required_roles = set([CommentsReader])
    column_names = "short_preview modified user owner *"
    stay_in_grid = True
    order_by = ["-modified"]
    label = _("Recent comments")
    preview_limit = 10
    display_mode = "summary"

    @classmethod
    def unused_param_defaults(cls, ar, **kw):
        # don't hide future comments. This can happen when I modify in a demo...
        kw = super(RecentComments, cls).param_defaults(ar, **kw)
        kw.update(observed_event=CommentEvents.modified)
        kw.update(end_date=dd.today())
        return kw

    @classmethod
    def unused_get_table_summary(cls, obj, ar):
        sar = cls.request_from(
            ar, master_instance=obj, limit=cls.preview_limit)

        # print "20170208", sar.limit
        html = ""
        items = []
        for o in sar.sliced_data_iterator:
            li = cls.as_li(o, ar)
            # if o.owner: #Catch for ownerless hackerish comments
            #     li += _(" On: ") + tostring(ar.obj2html(o.owner))

            # items.append("<li>{}</li>".format(li))
            items.append("<p>{}</p>".format(li))
            # items.append(li)
        # html += "<p>" + tostring(btn) + "</p>"

        if len(items) > 0:
            html += "<div>{0}</div>".format(''.join(items))

        return ar.html_text(html)

    @classmethod
    def get_table_summary(cls, obj, ar):
        # print("20190926 get_table_summary", ar.request)
        sar = cls.request_from(
            ar, master_instance=obj, limit=cls.preview_limit)

        # print "20170208", sar.limit
        chunks = []
        for o in sar.sliced_data_iterator:

            # by = _("{0} by {1}").format(
            #     naturaltime(o.created), str(o.user))

            if (o.modified - o.created).total_seconds() < 1:
                t = _("Created " + o.created.strftime('%Y-%m-%d %H:%M') )
            else:
                t = _("Modified " + o.modified.strftime('%Y-%m-%d %H:%M') )

            items = [ar.obj2html(o, naturaltime(o.created), title=t)]
            items += [" by ", ar.obj2html(o.user, o.user.username)]
            if o.owner_id:
                group = o.owner.get_comment_group()
                if group is not None:
                    items += ["@", ar.obj2html(group, group.ref)]
                # items += [" about ", ar.obj2html(o.owner)]
                items += [" about ", o.owner.obj2href(ar)]
            try:
                # el = etree.fromstring(o.short_preview, parser=html_parser)
                el = lxml.html.fragments_fromstring(o.short_preview) #, parser=cls.html_parser)
                # el = etree.fromstring("<div>{}</div>".format(o.full_preview), parser=cls.html_parser)
                # print(20190926, tostring(el))
            except Exception as e:
                el = [o.short_preview]
                # print(20190926, o.full_preview)
                el += " [{}]".format(e)
            # items += [" ", el]
            items += [" : "] + el

            chunks.append(E.p(*items))

        return E.div(*chunks)


    @classmethod
    def as_li(cls, self, ar):
        # chunks = [ar.parse_memo(self.short_preview)]

        by = _("{0} by {1}").format(
            naturaltime(self.created), str(self.user))

        if (self.modified - self.created).total_seconds() < 1:
            t = _("Created " + self.created.strftime('%Y-%m-%d %H:%M') )
        else:
            t = _("Modified " + self.modified.strftime('%Y-%m-%d %H:%M') )

        chunks = [tostring(ar.obj2html(self, by, title=t))]
        if self.owner_id:
            chunks += [" about ", tostring(ar.obj2html(self.owner))]
            chunks += [" on ", tostring(ar.obj2html(self.owner.site)), ")"]

        chunks += [self.full_preview]

        # if ar.get_user().authenticated:
        #     sar = cls.insert_action.request_from(ar)
        #     # print(20170217, sar)
        #     sar.known_values = dict(reply_to=self, owner=self.owner)
        #     if sar.get_permission():
        #         btn = sar.ar2button(
        #             None, _("Reply"), icon_name=None)
        #         chunks.append(' '+tostring(btn))

        html = ''.join(chunks)
        return html
        # return "<li>" + html + "</li>"



class CommentsByType(CommentsByX):
    master_key = 'comment_type'
    column_names = "body created user *"


class CommentsByRFC(CommentsByX):
    master_key = 'owner'
    column_names = "body created user *"
    stay_in_grid = True
    insert_layout = dd.InsertLayout("""
    reply_to
    # comment_type
    body
    """, window_size=(60, 13), hidden_elements="reply_to")


    @classmethod
    def get_table_summary(self, obj, ar):
        sar = self.request_from(ar, master_instance=obj)

        html = obj.get_rfc_description(ar)
        sar = self.insert_action.request_from(sar)
        if sar.get_permission():
            btn = sar.ar2button(None, _("Write comment"), icon_name=None)
            html += "<p>" + tostring(btn) + "</p>"

        html += "<ul>"
        for c in sar:
            html += "<li>{}<div id=\"{}\">{}</div></li>".format(
                self.get_comment_header(c, sar),
                "comment-" + str(c.id),
                ar.parse_memo(c.body))

        html += "</ul>"
        return ar.html_text(html)


def comments_by_owner(obj):
    return CommentsByRFC.request(master_instance=obj)
