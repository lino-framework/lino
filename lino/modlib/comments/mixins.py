# -*- coding: UTF-8 -*-
# Copyright 2015-2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from builtins import object

from django.db import models

from lino.api import dd, _
# from django.utils.translation import ugettext_lazy as _
# from lino.core.model import Model


class Commentable(dd.Model):
    class Meta(object):
        abstract = True

    # commentable_generic_relation = None

    private = models.BooleanField(_("Private"), default=False)

    def on_commented(self, comment, ar, cw):
        pass

    def get_rfc_description(self, ar):
        return ''

    def get_comment_group(self):
        return None

    @classmethod
    def add_comments_filter(cls, qs, user):
        """
        Override this to define your own privacy settings.
        Default behavious is that comments are visible only to real users (not to anonymous).
        Usage example in :class:`lino_noi.lib.tickets.Ticket`

        """
        if user.is_anonymous:
            qs = qs.none()
        return qs
