# -*- coding: UTF-8 -*-
# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Model mixin for `lino.modlib.dedupe`.

Note about the name: The first meaning of *to dupe somebody* is "to
make a dupe of; deceive; delude; trick." (`reference.com
<http://dictionary.reference.com/browse/dupe>`_). This is *not* the
meaning of our `Dupable` mixin. We use the second meaning: "to dupe
something" can also mean "to *duplicate* something".  This mixin is to
be used on models for which there is a danger of having duplicate
records. It is both for *avoiding* such duplicates on new records and
for *detecting* existing duplicates.


"""

from __future__ import unicode_literals

import fuzzy

DMETA = fuzzy.DMetaphone()

from django.db import models
# from django.db.models import Q

from lino.api import dd, rt, _
from lino.core.actions import SubmitInsert
# from itertools import combinations


def phonetic(s):
    # fuzzy.DMetaphone does not work with unicode strings
    # https://bitbucket.org/yougov/fuzzy/issue/2/fuzzy-support-for-unicode-strings-with
    return DMETA(s.encode('utf8'))[0]
    # return fuzzy.nysiis(s)


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
            msg = _("There are %d similar %s:") % (
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


class Dupable(dd.Model):
    """Adds a field `phonetic_words` and replaces `submit_insert` by
    :class:`CheckedSubmitInsert`.

    """
    class Meta:
        abstract = True

    submit_insert = CheckedSubmitInsert()

    # phonetic_words = models.CharField(_("Phonetic name"), max_length=200)

    def save(self, *args, **kwargs):
        super(Dupable, self).save(*args, **kwargs)
        # A related object set can be replaced in bulk with one
        # operation by assigning a new iterable of objects to it
        PhoneticWord = rt.modules.dedupe.PhoneticWord
        PhoneticWord.objects.filter(owner=self).delete()
        words = map(phonetic, self.get_dupable_words())
        for w in words:
            PhoneticWord(word=w, owner=self).save()
        # words = [PhoneticWord(word=w, owner=self) for w in words]
        # self.phonetic_words.clear()
        # self.phonetic_words = words
        # for w in words:
        #     w.save()

    def get_dupable_words(self):
        name = self.name
        for c in '-,/&+':
            name = name.replace(c, ' ')
        return name.split()

    def find_similar_instances(obj, *args, **kwargs):
        """This is Lino's default algorithm for finding similar humans in a
        database. It is rather simplistic. To become more smart, we
        might add helper tables with soundex copies of the names.

        """
        if obj.pk is None:
            return obj.__class__.objects.none()
        qs = obj.__class__.objects.exclude(pk=obj.pk).filter(*args, **kwargs)
        parts = map(phonetic, obj.get_dupable_words())
        qs = qs.filter(phonetic_words__word__in=parts).distinct()
        qs = qs.annotate(
            num=models.Count('phonetic_words__word'))
        qs = qs.filter(num__gte=2)
        # print("20150306 find_similar_instances %s" % qs.query)
        return qs


