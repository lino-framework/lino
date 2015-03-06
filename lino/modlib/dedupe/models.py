# -*- coding: UTF-8 -*-
# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Database models for `lino.modlib.dedupe`.

"""

from django.db import models
from lino.api import dd, _


class PhoneticWord(dd.Model):

    allow_cascaded_delete = ['owner']

    owner = dd.ForeignKey('contacts.Partner', related_name='phonetic_words')
    word = models.CharField(max_length=100)

    def __unicode__(self):
        return self.word


class PhoneticWords(dd.Table):
    model = 'dedupe.PhoneticWord'


class SimilarPartners(dd.VirtualTable):
    """See above."""
    label = _("Similar Partner")
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



# @dd.receiver(dd.pre_analyze)
# def dedupe_pre_analyze(sender=None, **kwargs):
#     Partner = rt.modules.contacts.Partner
#     dd.inject_field(Partner, 'phonetic_name',
#                     models.CharField(_("Phonetic name"), max_length=200))
#     dd.update_model(Partner, submit_insert=CheckedSubmitInsert())


# dd.inject_field('contacts.Partner', 'phonetic_name',
#                 models.CharField(_("Phonetic name"), max_length=200))
# dd.update_model('contacts.Partner', submit_insert=CheckedSubmitInsert())

# from lino.modlib.contacts.models import Partner
# from django.db.models.signals import pre_save

# @dd.receiver(pre_save, sender=Partner)
# def post_init_dedupe(sender, instance=None, **kwargs):
#     instance.phonetic_name = ' '.join([
#         fuzzy.nysiis(w) for w in instance.get_words()])
