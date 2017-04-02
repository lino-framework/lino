# -*- coding: UTF-8 -*-
# Copyright 2015-2017 Luc Saffre
# License: BSD (see file COPYING for details)
"""Database models for `lino.modlib.comments`.

"""
from builtins import object

from django.db import models

from lino.api import dd, _


class Commentable(dd.Model):
    """A request for comment. Every database model of an application"""
    class Meta(object):
        abstract = True

    private = models.BooleanField(_("Private"), default=False)
    
    def on_commented(self, comment, ar, cw):
        """This is automatically called when a comment has been created or
        modified.

        """
        pass
    
    def get_rfc_description(self, ar):
        """Return a HTML formatted string with the description of this
        Commentable as it should be displayed by the slave summary of
        CommentsByOwner.

        It must be a string and not an etree element. That's because
        it usually includes the content of RichTextField. If the API
        required an element, it would require us to parse this content
        just in order to generate HTML from it.

        """
        return ''

        
