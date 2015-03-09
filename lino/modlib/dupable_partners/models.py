# -*- coding: UTF-8 -*-
# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Database models for `lino.modlib.dupable_partners`.
"""

from lino.api import dd, _

from lino.mixins.dupable import DupableWordBase


class Word(DupableWordBase):
    """Phonetic words for Partners."""

    class Meta:
        verbose_name = _("Phonetic word")
        verbose_name_plural = _("Phonetic words")

    owner = dd.ForeignKey('contacts.Partner', related_name='dupable_words')


class Words(dd.Table):
    model = 'dupable_partners.Word'
    required = dd.Required(user_level='admin')


class SimilarPartners(dd.VirtualTable):
    """Shows the other partners who are similar to this one."""
    label = _("Similar partners")
    # slave_grid_format = 'html'
    slave_grid_format = 'summary'

    class Row:

        def __init__(self, master, other):
            self.master = master
            self.other = other

        def summary_row(self, ar):
            yield ar.obj2html(self.other)

        def __unicode__(self):
            return unicode(self.other)

    @classmethod
    def get_data_rows(self, ar):
        mi = ar.master_instance
        if mi is None:
            return

        for o in mi.find_similar_instances():
            yield self.Row(mi, o)

    @dd.displayfield(_("Other"))
    def other(self, obj, ar):
        return ar.obj2html(obj.other)

