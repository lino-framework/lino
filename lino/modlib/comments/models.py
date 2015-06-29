# -*- coding: UTF-8 -*-
# Copyright 2013-2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""Database models for `lino.modlib.comments`.

"""

import logging
logger = logging.getLogger(__name__)

from django.utils.translation import ugettext_lazy as _
from django.contrib.humanize.templatetags.humanize import naturaltime

from lino.modlib.contenttypes.mixins import Controllable

from lino.api import dd
from lino import mixins
from lino.modlib.users.mixins import ByUser, UserAuthored


class Comment(
        mixins.CreatedModified,
        UserAuthored,
        mixins.Hierarizable,
        Controllable):
    """The model definition."""

    class Meta:
        abstract = dd.is_abstract_model(__name__, 'Comment')
        verbose_name = _("Comment")
        verbose_name_plural = _("Comment")

    #~ text = dd.RichTextField(_("Text"),blank=True,format='html')
    text = dd.RichTextField(_("Text"), format='plain')

    def __unicode__(self):
        return u'%s #%s' % (self._meta.verbose_name, self.pk)

dd.update_field(Comment, 'user', editable=False)


class Comments(dd.Table):
    required_roles = dd.required(dd.SiteStaff)
    slave_grid_format = "summary"

    model = 'comments.Comment'

    insert_layout = dd.FormLayout("""
    text
    """, window_size=(40, 10))

    detail_layout = """
    id user created modified owner
    text
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


class CommentsByController(CommentsByX):
    master_key = 'owner'
    column_names = "text created user *"

    @classmethod
    def summary_row(cls, ar, obj, **kw):
        yield obj.text
        yield " ("
        yield ar.obj2html(obj, naturaltime(obj.created))
        yield _(" by ")
        yield ar.obj2html(obj.user)
        yield ")"


