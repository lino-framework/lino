# -*- coding: UTF-8 -*-
# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Database models for `lino.modlib.dupable_partners`.
"""

from lino.api import dd, _

from lino.mixins.dupable import DupableWordBase, SimilarObjects


class Word(DupableWordBase):
    """Phonetic words for Partners."""

    class Meta:
        verbose_name = _("Phonetic word")
        verbose_name_plural = _("Phonetic words")

    owner = dd.ForeignKey('contacts.Partner', related_name='dupable_words')


class Words(dd.Table):
    model = 'dupable_partners.Word'
    required = dd.Required(user_level='admin')


class SimilarPartners(SimilarObjects):
    label = _("Similar partners")

