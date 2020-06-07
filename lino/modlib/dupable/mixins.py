# -*- coding: UTF-8 -*-
# Copyright 2014-2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from builtins import map
from builtins import object

from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation

from lino.api import dd, rt, _
from lino.core.actions import SubmitInsert
from lino.core.gfks import gfk2lookup
from lino.core.gfks import ContentType


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

        qs = list(obj.find_similar_instances(4))
        if len(qs) > 0:
            msg = _("There are %d similar %s:") % (
                len(qs), obj._meta.verbose_name_plural)
            for other in qs:
                msg += '<br/>\n' + str(other)

            msg += '<br/>\n'
            msg += _("Are you sure you want to create a new "
                     "%(model)s named %(name)s?") % dict(
                model=obj._meta.verbose_name,
                name=obj.get_full_name())

            ar.confirm(ok, msg)
        else:
            ok(ar)

class Dupable(dd.Model):
    """Base class for models that can be "dupable".

    This mixin is to be used on models for which there is a danger of
    having unwanted duplicate records. It is both for *avoiding* such
    duplicates on new records and for *detecting* existing duplicates.

    """
    class Meta(object):
        abstract = True

    dupable_words = GenericRelation(
        'dupable.PhoneticWord',
        content_type_field='owner_type',
        object_id_field='owner_id')

    # show_words = dd.ShowSlaveTable('dupable.WordsByOwner')

    submit_insert = CheckedSubmitInsert()
    """A dupable model has its
    :attr:`submit_insert<lino.core.model.Model.submit_insert>` action
    overridden by :class:`CheckedSubmitInsert`, a extended variant of
    the action which checks for duplicate rows and asks a user
    confirmation when necessary.

    """

    dupable_words_field = 'name'
    """The name of a CharField on this model which holds the full-text
    description that is being tested for duplicates."""

    def dupable_matches_required(self):
        """Return the minimum number of words that must sound alike before
        two rows should be considered similar.

        """
        return 2

    def update_dupable_words(self, really=True):
        """Update the phonetic words of this row."""

        # Excerpt from Django docs: "A related object set can be
        # replaced in bulk with one operation by assigning a new
        # iterable of objects to it". But only when the relation is
        # nullable...
        if settings.SITE.loading_from_dump:
            return
        PhoneticWord = rt.models.dupable.PhoneticWord
        qs = PhoneticWord.objects.filter(
            **gfk2lookup(PhoneticWord.owner, self)).order_by('id')
        existing = [o.word for o in qs]
        wanted = list(self.get_dupable_words(
            getattr(self, self.dupable_words_field)))
        if existing == wanted:
            return
        if really:
            qs.delete()
            for w in wanted:
                PhoneticWord(word=w, owner=self).save()
        return _("Must update phonetic words.")
        # return _("(existing {}, wanted {})").format(existing, wanted)

    def after_ui_save(self, ar, cw):
        super(Dupable, self).after_ui_save(ar, cw)
        if cw is None or cw.has_changed(self.dupable_words_field):
            self.update_dupable_words()

    def get_dupable_words(self, s):
        for c in '-,/&+':
            s = s.replace(c, ' ')
        return filter(
            None, map(
                rt.models.dupable.PhoneticWord.reduce_word,
                s.split()))

    def find_similar_instances(self, limit=None, **kwargs):
        """Return a queryset or yield a list of similar objects.

        If `limit` is specified, we never want to see more than
        `limit` duplicates.

        Note that an overridden version of this method might return a
        list or generator instead of a Django queryset.

        """
        qs = self.__class__.objects.filter(**kwargs)
        if self.pk is not None:
            qs = qs.exclude(pk=self.pk)
        parts = self.get_dupable_words(
            getattr(self, self.dupable_words_field))
        if False:
            fkw = gfk2lookup(rt.models.dupable.PhoneticWord.owner, self)
            wq = rt.models.dupable.PhoneticWord.objects.filter(**fkw)
            wq = wq.filter(word__in=parts).distinct()
            qs = qs.annotate(num=models.Count('dupable_words__word'))
            # ct = ContentType.objects.get_for_model(self.__class__)
            # qs = qs.filter(owner_type=ct)
        if True:
            qs = qs.filter(dupable_words__word__in=parts).distinct()
            qs = qs.annotate(num=models.Count('dupable_words__word'))
        qs = qs.filter(num__gte=self.dupable_matches_required())
        qs = qs.order_by('-num', 'pk')
        # print("20150306 find_similar_instances %s" % qs.query)
        if limit is None:
            return qs
        return qs[:limit]





from lino.modlib.checkdata.choicelists import Checker


class DupableChecker(Checker):
    """Checks for the following repairable problem:

    - :message:`Must update phonetic words.`

    """
    verbose_name = _("Check for missing phonetic words")
    model = Dupable

    def get_checkdata_problems(self, obj, fix=False):
        msg = obj.update_dupable_words(fix)
        if msg:
            yield (True, msg)


DupableChecker.activate()

class SimilarObjectsChecker(Checker):
    model = Dupable
    verbose_name = _("Check for similar objects")

    def get_checkdata_problems(self, obj, fix=False):
        lst = list(obj.find_similar_instances(1))
        if len(lst):
            msg = _("Similar clients: {clients}").format(
                clients=', '.join(map(str, lst)))
            yield (False, msg)

SimilarObjectsChecker.activate()
