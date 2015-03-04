# -*- coding: UTF-8 -*-
# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Database models for `lino.modlib.dedupe`.

"""

from __future__ import unicode_literals

from lino.api import dd, _


class SimilarPartners(dd.VirtualTable):
    """See above."""
    label = _("Similar Partner")
    # slave_grid_format = 'html'
    slave_grid_format = 'summary'

    class Row:

        def __init__(self, master, slave):
            self.master = master
            self.slave = slave

        def summary_row(self, ar):
            yield ar.obj2html(self.slave)

        def __unicode__(self):
            return unicode(self.slave)

    @classmethod
    def get_data_rows(self, ar):
        mi = ar.master_instance
        if mi is None:
            return

        for o in mi.find_similar_instances():
            yield self.Row(mi, o)

    @dd.displayfield(_("Other"))
    def other(self, obj, ar):
        return ar.obj2html(obj.slave)



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
