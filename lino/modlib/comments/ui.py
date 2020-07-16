# -*- coding: UTF-8 -*-
# Copyright 2013-2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from django.utils.translation import ugettext_lazy as _
from django.contrib.humanize.templatetags.humanize import naturaltime

from lino.api import dd, rt
from lino.modlib.users.mixins import My
from etgen.html import E, tostring
# from lxml import etree
import lxml
# from lino.utils.soup import truncate_comment
from lino.core.gfks import gfk2lookup
from .roles import CommentsReader, CommentsUser, CommentsStaff
from .choicelists import CommentEvents
from lino import mixins
from lino.core.constants import CHOICES_BLANK_FILTER_VALUE


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
    params_layout = "start_date end_date observed_event user reply_to"

    insert_layout = dd.InsertLayout("""
    reply_to owner owner_type owner_id
    # comment_type
    body
    private
    """, window_size=(60, 13), hidden_elements="reply_to owner owner_type owner_id")

    detail_layout = """
    id user created modified private
    reply_to owner owner_type owner_id comment_type
    body
    CommentsByComment
    """

    # html_parser = etree.HTMLParser()

    # ~ column_names = "id date user type event_type subject * body_html"
    # ~ column_names = "id date user event_type type project subject * body"
    # ~ hide_columns = "body"
    # ~ hidden_columns = frozenset(['body'])
    # ~ order_by = ["id"]
    # ~ label = _("Notes")

    @classmethod
    def get_simple_parameters(cls):
        for p in super(Comments, cls).get_simple_parameters():
            yield p
        yield "reply_to"

    @classmethod
    def get_table_summary(cls, obj, ar):
        # print("20190926 get_table_summary", ar.request)
        sar = cls.request_from(ar, master_instance=obj, limit=cls.preview_limit)
        # print "20170208", sar.limit
        # chunks = []
        # for o in sar.sliced_data_iterator:
        #     chunks.append(E.p(*o.as_summary_row(ar)))
        # return E.div(*chunks)
        chunks = [o.as_summary_row(ar) for o in sar.sliced_data_iterator]
        html = '\n'.join(chunks)
        return "<div>{}</div>".format(html)

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
        if ar.get_user().is_authenticated:
            btn = sar.ar2button(None, _(" Reply "), icon_name=None)
            # btn.set("style", "padding-left:10px")
            ch += [" [", btn, "]"]

        # ch.append(' ')
        # ch.append(
        #     E.a(u"⁜", onclick="toggle_visibility('comment-{}');".format(
        #         comment.id), title=str(_("Hide")), href="#")
        # )
        return tostring(ch)

    # @classmethod
    # def as_li(cls, self, ar):
    #     # chunks = [ar.parse_memo(self.short_preview)]
    #     chunks = [self.short_preview]
    #
    #     by = _("{0} by {1}").format(
    #         naturaltime(self.created), str(self.user))
    #
    #     if (self.modified - self.created).total_seconds() < 1:
    #         t = _("Created " + self.created.strftime('%Y-%m-%d %H:%M') )
    #     else:
    #         t = _("Modified " + self.modified.strftime('%Y-%m-%d %H:%M') )
    #
    #     chunks += [
    #         " (", tostring(ar.obj2html(self, by, title=t)), ")"
    #     ]
    #     # if self.more_text:
    #     #     chunks.append(" (...)")
    #
    #     if ar.get_user().authenticated:
    #         sar = cls.insert_action.request_from(ar)
    #         # print(20170217, sar)
    #         sar.known_values = dict(reply_to=self, owner=self.owner)
    #         if sar.get_permission():
    #             btn = sar.ar2button(
    #                 None, _("Reply"), icon_name=None)
    #             chunks.append(' '+tostring(btn))
    #
    #
    #     html = ''.join(chunks)
    #     return html
    #     # return "<li>" + html + "</li>"


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
    # order_by = ["-modified"]
    display_mode = "summary"
    card_layout = dd.DetailLayout("""
    card_summary
    CommentsByComment
    """)

    @classmethod
    def get_card_title(self, ar, obj):
        """Overrides the default behaviour
        """
        return ar.actor.get_comment_header(obj, ar)


# class MyPendingComments(MyComments):
#     label = _("My pending comments")
#     welcome_message_when_count = 0

#     @classmethod
#     def param_defaults(cls, ar, **kw):
#         kw = super(MyPendingComments, cls).param_defaults(ar, **kw)
#         kw.update(show_published=dd.YesNo.no)
#         return kw

class RecentComments(CommentsByX):
    required_roles = dd.login_required(CommentsReader)
    # required_roles = set([CommentsReader])
    column_names = "short_preview modified user owner *"
    stay_in_grid = True
    # order_by = ["-modified"]
    label = _("Recent comments")
    preview_limit = 10
    # display_mode = "summary"


class CommentsByType(CommentsByX):
    master_key = 'comment_type'
    column_names = "body created user *"


class CommentsByRFC(CommentsByX):
    master_key = 'owner'
    column_names = "body created user *"
    stay_in_grid = True
    display_mode = "list"
    simple_slavegrid_header = True
    insert_layout = dd.InsertLayout("""
    reply_to
    # comment_type
    body
    private
    """, window_size=(60, 13), hidden_elements="reply_to")

    @classmethod
    def param_defaults(cls, ar, **kw):
        kw = super(CommentsByRFC, cls).param_defaults(ar, **kw)
        kw['reply_to'] = CHOICES_BLANK_FILTER_VALUE
        return kw

    @classmethod
    def get_main_card(self, ar):
        ticket_obj = ar.master_instance
        sar = self.request_from(ar, master_instance=ticket_obj)
        html=ticket_obj.get_rfc_description(ar)
        sar = self.insert_action.request_from(sar)
        if sar.get_permission():
            btn = sar.ar2button(None, _("Write comment"), icon_name=None)
            html += "<p>" + tostring(btn) + "</p>"

        if html:
            return dict(
                card_title="Description",
                main_card_body=html, # main_card_body is special keyword
                id="[main_card]" # needed for map key in react...
            )
        else:
            return None

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


class CommentsByMentioned(CommentsByX):
    # show all comments that mention the master instance
    master = dd.Model
    label = _("Mentions")

    # label = _("Comments mentioning this")

    @classmethod
    def get_filter_kw(cls, ar, **kw):
        mi = ar.master_instance
        if mi is None:
            return None
        Mention = rt.models.comments.Mention
        mkw = gfk2lookup(Mention.owner, mi)
        mentions = Mention.objects.filter(**mkw).values_list('comment_id', flat=True)
        # mentions = [o.comment_id for o in Mention.objects.filter(**mkw)]
        # print(mkw, mentions)
        # return super(CommentsByMentioned, cls).get_filter_kw(ar, **kw)
        kw.update(id__in=mentions)
        return kw


class CommentsByComment(CommentsByX):
    master_key = 'reply_to'
    display_mode = "list"
    stay_in_grid = True
    borderless_list_mode = True
    title = _("Replies")
    simple_slavegrid_header = True

    paginator_template = "PrevPageLink NextPageLink"
    hide_if_empty = True


def comments_by_owner(obj):
    return CommentsByRFC.request(master_instance=obj)


class Mentions(dd.Table):
    required_roles = dd.login_required(CommentsStaff)
    model = "comments.Mention"
    column_names = "comment owner created *"
    detail_layout = """
    id comment owner created
    """


class MentionsByOwner(Mentions):
    master_key = "owner"
