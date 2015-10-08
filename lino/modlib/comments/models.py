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

from lino.modlib.gfks.mixins import Controllable

from lino.api import dd, rt
from lino import mixins
from lino.modlib.users.mixins import ByUser, UserAuthored
from lino.utils.xmlgen.html import E
from lino.core.utils import gfk2lookup

ALLOWED_TAGS = ['a', 'b', 'i', 'em']


def html2li(html):
    # html = obj.short_text
    html = bleach.clean(
        html, tags=ALLOWED_TAGS, strip=True)
    return "<span>" + html + "</span>"


class Comment(
        mixins.CreatedModified,
        UserAuthored,
        # mixins.Hierarchical,
        Controllable):
    """The model definition."""

    class Meta:
        abstract = dd.is_abstract_model(__name__, 'Comment')
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    short_text = dd.RichTextField(_("Short text"))
    more_text = dd.RichTextField(_("More text"), blank=True)

    def __unicode__(self):
        return u'%s #%s' % (self._meta.verbose_name, self.pk)

dd.update_field(Comment, 'user', editable=False)


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
    #~ master_key = 'user'
    #~ column_names = "date event_type type subject project body *"
    #~ column_names = "date event_type type subject body *"
    #~ column_names = "date type event_type subject body_html *"
    #~ can_view = perms.is_authenticated
    #~ label = _("My notes")
    order_by = ["created"]


class CommentsByX(Comments):
    required_roles = dd.required()
    #~ column_names = "date event_type type subject body user *"
    order_by = ["-created"]

USE_ETREE = False


class CommentsByController(CommentsByX):
    master_key = 'owner'
    column_names = "short_text created user *"
    stay_in_grid = True

    # @classmethod
    # def summary_row(cls, ar, obj, **kw):
    #     yield obj.text
    #     yield " ("
    #     yield ar.obj2html(obj, naturaltime(obj.created))
    #     yield _(" by ")
    #     yield ar.obj2html(obj.user)
    #     yield ")"

    @classmethod
    def get_slave_summary(self, obj, ar):
        """The :meth:`summary view <lino.core.actors.Actor.get_slave_summary>`
        for :class:`CommentsByController`.

        """
        sar = self.request_from(ar, master_instance=obj)

        elems = []

        if USE_ETREE:
            elems.append(E.raw(obj.description))
        else:
            if obj.description:
                elems.append(obj.description)

        items = []
        for obj in sar:
            if bleach is None:
                chunks = (
                    E.raw(obj.short_text),
                    " (",
                    ar.obj2html(obj, naturaltime(obj.created)),
                    unicode(_(" by ")),
                    ar.obj2html(obj.user), ")"
                )
            else:
                html = html2li(obj.short_text)
                # print html
                by = _("{0} by {1}").format(
                    naturaltime(obj.created), unicode(obj.user)),
                if USE_ETREE:
                    chunks = [
                        E.raw(html.encode('utf-8')),
                        " (", ar.obj2html(obj, by), ")"
                    ]
                else:
                    chunks = [
                        html,
                        " (", E.tostring(ar.obj2html(obj, by)), ")"
                    ]

                if obj.more_text:
                    chunks.append(" (...)")
            if USE_ETREE:
                items.append(E.li(*chunks))
            else:
                items.append(u"<li>{0}</li>".format(''.join(chunks)))
        if len(items) > 0:
            if USE_ETREE:
                elems.append(E.ul(*items))
            else:
                elems.append(u"<ul>{0}</ul>".format(''.join(items)))
        else:
            elems.append(_("No comments."))

        # Button for creating a new comment:

        sar = self.insert_action.request_from(sar)
        if ar.renderer.is_interactive and sar.get_permission():
            # gfk = rt.modules.comments.Comment.owner
            # sar.known_values.update(gfk2lookup(gfk, obj))
            btn = sar.ar2button(None, _("Write comment"), icon_name=None)
            if USE_ETREE:
                elems += [E.br(), btn]
            else:
                elems.append("<br/>" + E.tostring(btn))
        if USE_ETREE:
            return E.div(*elems, class_="htmlText")
        else:
            return u"""<div class="htmlText">{0}</div>""".format(
                ''.join(elems))
            

