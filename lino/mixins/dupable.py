# -*- coding: UTF-8 -*-
# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Defines the :class:`Dupable` model mixin and related functionality
to assist users in finding duplicate database records.

Used by :mod:`lino.modlib.dupable_partners`.

The current implementation of the detection algorithm uses the `fuzzy
<https://pypi.python.org/pypi/Fuzzy>`_ module. Read also Doug Hellmann
about `Using Fuzzy Matching to Search by Sound with Python
<http://www.informit.com/articles/article.aspx?p=1848528>`_

"""

from __future__ import unicode_literals

import fuzzy

DMETA = fuzzy.DMetaphone()

from django.conf import settings
from django.db import models
# from django.db.models import Q

from lino.api import dd, rt, _
from lino.core.actions import SubmitInsert


def phonetic(s):
    # fuzzy.DMetaphone does not work with unicode strings, see
    # https://bitbucket.org/yougov/fuzzy/issue/2/fuzzy-support-for-unicode-strings-with
    dm = DMETA(s.encode('utf8'))
    dms = dm[0] or dm[1]
    if dms is None:
        return ''
    return dms.decode('utf8')
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


class DupableWordBase(dd.Model):
    """Base class for the table of phonetic words of a given dupable
    model. For every (non-abstract) dupable model there must be a
    subclass of DupableWordBase. The subclass must define a field
    :attr:`owner` which points to the Dupable. And the
    :attr:`dupable_word_model`,

    """
    class Meta:
        abstract = True

    allow_cascaded_delete = ['owner']

    word = models.CharField(max_length=100)

    def __unicode__(self):
        return self.word


class Dupable(dd.Model):
    """Base class for models that can be "dupable".

    This mixin is to be used on models for which there is a danger of
    having unwanted duplicate records. It is both for *avoiding* such
    duplicates on new records and for *detecting* existing duplicates.

    Note about the name: to dupe *somebody* means "to make a dupe of;
    deceive; delude; trick." (`reference.com
    <http://dictionary.reference.com/browse/dupe>`_), while to dupe
    *something* means to duplicate it (eventually in order to cheat
    somebody e.g. by making a cheap copy of a valuable object).


    """
    class Meta:
        abstract = True

    submit_insert = CheckedSubmitInsert()
    """A dupable model has its :attr:`submit_insert
    <lino.core.model.Model.submit_insert>` action overridden by
    :class:`CheckedSubmitInsert`, a extended variant of the action
    which checks for duplicate rows and asks a user confirmation when
    necessary.

    """

    dupable_words_field = 'name'
    """The name of a CharField on this model which holds the full-text
    description that is being tested for duplicates."""

    dupable_matches_required = 2
    """Minimum number of words that must sound alike before two rows
    should be considered asimilar.

    """

    dupable_word_model = None

    # def save(self, *args, **kwargs):
    #     super(Dupable, self).save(*args, **kwargs)

    # Overriding name_changed won't work because we don't know whether
    # parent has a `name_changed` methdod:
    # def name_changed(self, ar):
    #     super(Dupable, self).name_changed(ar)
    #     self.update_dupable_words()

    @classmethod
    def on_analyze(cls, site):
        """Setup the :attr:`dupable_word_model` attribute.  This will be
        called only on concrete subclasses.

        """
        super(Dupable, cls).on_analyze(site)
        # if not site.is_installed(cls._meta.app_label):
        #     cls.dupable_word_model = None
        #     return
        site.setup_model_spec(cls, 'dupable_word_model')

    def update_dupable_words(self):
        """Update the dupable words of this row."""
        # "A related object set can be replaced in bulk with one
        # operation by assigning a new iterable of objects to it". But
        # only when the relatin is nullable...
        if settings.SITE.loading_from_dump:
            return
        if self.dupable_word_model is None:
            return
        qs = self.dupable_word_model.objects.filter(owner=self)
        existing = [o.word for o in qs]
        wanted = map(phonetic, self.get_dupable_words())
        if existing == wanted:
            return
        qs.delete()
        for w in wanted:
            self.dupable_word_model(word=w, owner=self).save()

    def after_ui_save(self, ar, cw):
        super(Dupable, self).after_ui_save(ar, cw)
        if cw is None or cw.has_changed(self.dupable_words_field):
            self.update_dupable_words()

    def get_dupable_words(self):
        name = getattr(self, self.dupable_words_field)
        for c in '-,/&+':
            name = name.replace(c, ' ')
        return name.split()

    def find_similar_instances(self, *args, **kwargs):
        """
        """
        if self.dupable_word_model is None:
            return self.__class__.objects.none()
        qs = self.__class__.objects.filter(*args, **kwargs)
        if self.pk is not None:
            qs = qs.exclude(pk=self.pk)
        parts = map(phonetic, self.get_dupable_words())
        qs = qs.filter(dupable_words__word__in=parts).distinct()
        qs = qs.annotate(num=models.Count('dupable_words__word'))
        qs = qs.filter(num__gte=self.dupable_matches_required)
        qs = qs.order_by('-num', 'pk')
        # print("20150306 find_similar_instances %s" % qs.query)
        return qs


# @dd.receiver(dd.pre_analyze)
# def setup_dupable_handlers(sender=None, request=None, **kw):

# @dd.receiver(dd.on_ui_updated(sender=Dupable))
# def on_dupable_update(sender=None, request=None, **kw):

#     if 'name' in sender.get_updates():
#         sender.watched.update_dupable_words()


def update_all_dupable_words():
    """To be called after initializing a demo database, e.g. from
    `lino_welfare.fixtures.demo2`.

    """
    raise Exception("Not yet used. Maybe once as an action on SiteConfig.")
    for m in settings.SITE.models_by_base(Dupable):
        for obj in m.objects.all():
            obj.update_dupable_words()
