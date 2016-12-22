# -*- coding: UTF-8 -*-
# Copyright 2013-2016 Luc Saffre
# License: BSD (see file COPYING for details)
"""Database models for `lino.modlib.comments`.

"""
from builtins import str
from builtins import object

import logging
logger = logging.getLogger(__name__)

from django.utils.translation import ugettext_lazy as _
from django.contrib.humanize.templatetags.humanize import naturaltime

from lino.api import dd
from lino.mixins import CreatedModified
from lino.modlib.users.mixins import UserAuthored
from lino.modlib.gfks.mixins import Controllable
from lino.modlib.notify.mixins import ChangeObservable
from lino.utils.xmlgen.html import E
from lino.mixins.bleached import Bleached

@dd.python_2_unicode_compatible
class Comment(CreatedModified, UserAuthored, Controllable,
              ChangeObservable, Bleached):
    """A **comment** is a short text which some user writes about some
    other database object. It has no recipient.

    .. attribute:: short_text

        A short "abstract" of your comment. This should not be more
        than one paragraph.

    """
    
    # ALLOWED_TAGS = ['a', 'b', 'i', 'em', 'ul', 'ol', 'li']
    
    class Meta(object):
        app_label = 'comments'
        abstract = dd.is_abstract_model(__name__, 'Comment')
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    short_text = dd.RichTextField(_("Short text"))
    more_text = dd.RichTextField(_("More text"), blank=True)

    def __str__(self):
        return u'%s #%s' % (self._meta.verbose_name, self.pk)

    def get_change_observers(self):
        if isinstance(self.owner, ChangeObservable):
            obs = self.owner
        else:
            obs = super(Comment, self)
        for u in obs.get_change_observers():
            yield u

    def get_notify_message(self, ar, cw):
        if cw is not None:
            return super(Comment, self).get_notify_message(ar, cw)
        s = _("{user} commented on {obj}:").format(
            user=ar.get_user(), obj=self.owner)
        s += ' ' + self.short_text
        if False:
            s += '\n<p>\n' + self.more_text
        return s

    # def get_notify_owner(self, ar):
    #     return self.owner

    def as_li(self, ar):
        """Return this comment as a list item. 

        """
        chunks = [ar.parse_memo(self.short_text)]
        by = _("{0} by {1}").format(
            naturaltime(self.created), str(self.user)),
        chunks += [
            " (", E.tostring(ar.obj2html(self, by)), ")"
        ]
        if self.more_text:
            chunks.append(" (...)")

        html = ''.join(chunks)
        return "<li>" + html + "</li>"

dd.update_field(Comment, 'user', editable=False)


from .ui import *
