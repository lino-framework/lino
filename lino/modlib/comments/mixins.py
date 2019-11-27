# -*- coding: UTF-8 -*-
# Copyright 2015-2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from django.db import models
from django.db.models import Q

from lino.api import dd, _

from .roles import PrivateCommentsReader

class Commentable(dd.Model):
    class Meta(object):
        abstract = True

    def on_commented(self, comment, ar, cw):
        pass

    def get_rfc_description(self, ar):
        return ''

    def get_comment_group(self):
        return None

    @classmethod
    def get_comments_filter(cls, user):
        if user.user_type.has_required_roles([PrivateCommentsReader]):
            return None
        if user.is_anonymous:
            return Q(private=False)
        return Q(private=False) | Q(user=user)

    def is_comment_private(self, comment, ar):
        """Whether the given comment should be private."""
        return dd.plugins.comments.private_default
