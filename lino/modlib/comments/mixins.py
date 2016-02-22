# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""Database models for `lino.modlib.comments`.

"""
from builtins import object

from lino.api import dd


class RFC(dd.Model):
    """A request for comment. Every database model of an application """
    class Meta(object):
        abstract = True

    def get_rfc_description(self, ar):
        """Return a HTML formatted string with the description of this RFC as
        it should be displayed by the slave summary of
        CommentsByOwner.

        It must be a string and not an etree element. That's because
        it usually includes the content of RichTextField. If the API
        required an element, it would require us to parse this content
        just in order to generate HTML from it)

        """
        return ''


