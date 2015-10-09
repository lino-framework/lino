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




class Comment(
        mixins.CreatedModified,
        UserAuthored,
        # mixins.Hierarchical,
        Controllable):
    """A **comment** is a short text which some user writes about some
    other database object.

    .. attribute:: short_text

        A short "abstract" of your comment. This should not be more
        than one paragraph.

    """

    ALLOWED_TAGS = ['a', 'b', 'i', 'em']

    class Meta:
        abstract = dd.is_abstract_model(__name__, 'Comment')
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    short_text = dd.RichTextField(_("Short text"))
    more_text = dd.RichTextField(_("More text"), blank=True)

    def __unicode__(self):
        return u'%s #%s' % (self._meta.verbose_name, self.pk)

    def as_li(self, ar):
        """Return this comment as a list item. If `bleach
        <http://bleach.readthedocs.org/en/latest/>`_ is installed, all
        tags except some will be removed when

        """
        if bleach is None:
            chunks = [self.short_text]
        else:
            chunks = [bleach.clean(
                self.short_text, tags=self.ALLOWED_TAGS, strip=True)]

        by = _("{0} by {1}").format(
            naturaltime(self.created), unicode(self.user)),
        chunks += [
            " (", E.tostring(ar.obj2html(self, by)), ")"
        ]
        if self.more_text:
            chunks.append(" (...)")

        html = ''.join(chunks)
        return "<li>" + html + "</li>"

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
    """Shows the comments of a given database object.
    """
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

        html = obj.description
        items = [o.as_li(ar) for o in sar]
        if len(items) > 0:
            html += u"<ul>{0}</ul>".format(''.join(items))

        sar = self.insert_action.request_from(sar)
        if ar.renderer.is_interactive and sar.get_permission():
            btn = sar.ar2button(None, _("Write comment"), icon_name=None)
            html += "<p>" + E.tostring(btn) + "</p>"
        return u"""<div class="htmlText">{0}</div>""".format(html)
            

def comments_by_owner(obj):
    return CommentsByController.request(master_instance=obj)
