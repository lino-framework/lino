# -*- coding: UTF-8 -*-
# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Model mixin for `lino.modlib.dedupe`.


"""

from __future__ import unicode_literals

import fuzzy

from django.db import models
from django.db.models import Q

from lino.api import dd, rt, _
from lino.core.actions import SubmitInsert
from itertools import combinations


class CheckedSubmitInsert(SubmitInsert):
    """Like the standard :class:`lino.core.actions.SubmitInsert`, but adds
    a confirmation if there is a possible duplicate record.

    """
    def run_from_ui(self, ar, **kw):
        obj = ar.create_instance_from_request()

        def ok(ar2):
            self.save_new_instance(ar2, obj)
            ar2.set_response(close_window=True)
            # logger.info("20140512 CheckedSubmitInsert")

        qs = obj.find_similar_instances()
        if qs.count() > 0:
            msg = _("There are %d %s with similar name:") % (
                qs.count(), qs.model._meta.verbose_name_plural)
            for other in qs[:4]:
                msg += '<br/>\n' + unicode(other)

            msg += '<br/>\n'
            msg += _("Are you sure you want to create a new "
                     "%(model)s named %(name)s?") % dict(
                model=qs.model._meta.verbose_name,
                name=obj.get_full_name())

            ar.confirm(ok, msg)
        else:
            ok(ar)


class Dedupable(dd.Model):
    """Adds a field `phonetic_name` and replaces `submit_insert` by
    :class:`CheckedSubmitInsert`.

    """
    class Meta:
        abstract = True

    submit_insert = CheckedSubmitInsert()

    phonetic_name = models.CharField(_("Phonetic name"), max_length=200)

    def full_clean(self):
        self.phonetic_name = ' '.join([
            fuzzy.nysiis(w) for w in self.get_words()])
        super(Dedupable, self).full_clean()

    def get_words(self):
        name = self.name
        for c in '-,/&+':
            name = name.replace(c, ' ')
        return name.split()
        # s1 = set()
        # for word in name.split():
        #     s1.add(word)
        # s2 = set()
        # for n in s1:
        #     for word in n.split('-'):
        #         s2.add(word)
        # return s2

    def find_similar_instances(obj):
        """This is Lino's default algorithm for finding similar humans in a
        database. It is rather simplistic. To become more smart, we
        might add helper tables with soundex copies of the names.

        """
        qs = rt.modules.contacts.Partner.objects.exclude(pk=obj.pk)
        cnd = Q()
        parts = [fuzzy.nysiis(w) for w in obj.get_words()]
        for comb in combinations(parts, 2):
            cnd |= (
                Q(phonetic_name__icontains=comb[0]) &
                Q(phonetic_name__icontains=comb[1]))
        if cnd:
            # logger.info("20140222 find_similar_instances word %s", w)
            qs = qs.filter(cnd)
        # logger.info("20140222 find_similar_instances %s", qs.query)
        return qs


