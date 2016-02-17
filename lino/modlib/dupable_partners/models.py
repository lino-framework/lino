# -*- coding: UTF-8 -*-
# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Database models for `lino.modlib.dupable_partners`.
"""
from builtins import object

from lino.api import dd, _

from lino.mixins.dupable import PhoneticWordBase, SimilarObjects


class Word(PhoneticWordBase):
    """Phonetic words for Partners."""

    class Meta(object):
        verbose_name = _("Phonetic word")
        verbose_name_plural = _("Phonetic words")

    owner = dd.ForeignKey('contacts.Partner', related_name='dupable_words')


class Words(dd.Table):
    model = 'dupable_partners.Word'
    required_roles = dd.required(dd.SiteStaff)


class SimilarPartners(SimilarObjects):
    label = _("Similar partners")

