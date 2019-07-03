# -*- coding: UTF-8 -*-
# Copyright 2014-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""
Defines the :class:`Dupable` model mixin and related functionality
to assist users in finding unwanted duplicate database records.

Don't mix up this module with :mod:`lino.mixins.duplicable`.  Models
are "duplicable" if users may *want* to duplicate some instance
thereof, while "dupable" implies that the duplicates are *unwanted*.
To dupe *somebody* means "to make a dupe of; deceive; delude; trick."
(`reference.com <http://dictionary.reference.com/browse/dupe>`_), and
to dupe *something* means to duplicate it (eventually in order to
cheat somebody e.g. by making a cheap copy of a valuable object).

This requires the `metafone
<https://pypi.python.org/pypi/Metafone/0.5>`__ package (a successor of
`fuzzy <https://pypi.python.org/pypi/Fuzzy>`__ which isn't yet ported
to Python 3).  Applications that use this mixin must themselves add
`metafone` to their :ref:`install_requires`.

The current implementation uses a helper table with "phonetic words"
and the `Double Metaphone
<https://en.wikipedia.org/wiki/Metaphone#Double_Metaphone>`_
algorithm.  Read also Doug Hellmann about `Using Fuzzy Matching to
Search by Sound with Python
<http://www.informit.com/articles/article.aspx?p=1848528>`_
(2012-03-22) and `Phonetic Similarity of Words: A Vectorized Approach
in Python
<http://stackabuse.com/phonetic-similarity-of-words-a-vectorized-approach-in-python/>`__
by Frank Hofmann (2018-02-12)
"""

from __future__ import unicode_literals
import six
from builtins import map
from builtins import str
from builtins import object

from django.conf import settings
from django.db import models

from lino.api import dd, _
from lino.core.actions import SubmitInsert
from lino.utils import join_elems
from etgen.html import E


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


from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class PhoneticWordBase(dd.Model):
    """Base class for the table of phonetic words of a given dupable
    model. For every (non-abstract) dupable model there must be a
    subclass of `PhoneticWordBase`.
    The subclass must define a field
    :attr:`owner` which points to the `Dupable`, and the `Dupable`'s
    :attr:`dupable_word_model` must point to its subclass
    of `PhoneticWordBase`.

    """
    class Meta(object):
        abstract = True

    allow_cascaded_delete = ['owner']

    word = models.CharField(max_length=100)

    def __str__(self):
        return self.word

    # @classmethod
    # def on_analyze(cls, site):
    #     pass
        # import metaphone as fuzzy
        # cls._fuzzy_DMetaphone = fuzzy.doublemetaphone()
        # import fuzzy
        # cls._fuzzy_DMetaphone = fuzzy.DMetaphone()

    @classmethod
    def reduce_word(cls, s):
        # from metaphone.word import Word
        import metaphone as fuzzy
        # fuzzy.DMetaphone does not work with unicode strings, see
        # https://bitbucket.org/yougov/fuzzy/issue/2/fuzzy-support-for-unicode-strings-with
        # dm = fuzzy.doublemetaphone(s.encode('utf8'))
        dm = fuzzy.doublemetaphone(s)
        dms = dm[0] or dm[1]
        if dms is None:
            return ''
        if isinstance(dms, six.binary_type):
            dms = dms.decode('utf8')
        return dms


class Dupable(dd.Model):
    """
    Base class for models that can be "dupable".

    This mixin is to be used on models for which there is a danger of
    having unwanted duplicate records. It is both for *avoiding* such
    duplicates on new records and for *detecting* existing duplicates.

    Note that adding :class:`Dupable` to your model's base classes
    does not yet activate any functionality, it just declares that
    model as being dupable.  In order to activate verification, you
    must also define a model which implements
    :class:`PhoneticWordBase` and set
    :attr:`Dupable.dupable_word_model` to point to that model.  This
    is done by plugins like :mod:`lino_xl.lib.dupable_partners` or
    :mod:`lino_welfare.modlib.dupable_clients`
    """
    class Meta(object):
        abstract = True

    submit_insert = CheckedSubmitInsert()
    """
    A dupable model has its
    :attr:`submit_insert<lino.core.model.Model.submit_insert>` action
    overridden by :class:`CheckedSubmitInsert`, a extended variant of
    the action which checks for duplicate rows and asks a user
    confirmation when necessary.
    """

    dupable_words_field = 'name'
    """The name of a CharField on this model which holds the full-text
    description that is being tested for duplicates."""

    dupable_word_model = None
    """Full name of the model used to hold dupable words for instances of
    this model.  Applications can specify a string which will be
    resolved at startup to the model's class object.

    """

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
        if self.dupable_word_model is None:
            return
        qs = self.dupable_word_model.objects.filter(owner=self)
        existing = [o.word for o in qs]
        wanted = self.get_dupable_words(
            getattr(self, self.dupable_words_field))
        if existing == wanted:
            return
        if really:
            qs.delete()
            for w in wanted:
                self.dupable_word_model(word=w, owner=self).save()
        return _("Must update phonetic words.")

    def after_ui_save(self, ar, cw):
        super(Dupable, self).after_ui_save(ar, cw)
        if cw is None or cw.has_changed(self.dupable_words_field):
            self.update_dupable_words()

    def get_dupable_words(self, s):
        for c in '-,/&+':
            s = s.replace(c, ' ')
        return list(map(self.dupable_word_model.reduce_word, s.split()))

    def find_similar_instances(self, limit=None, **kwargs):
        """Return a queryset or yield a list of similar objects.

        If `limit` is specified, we never want to see more than
        `limit` duplicates.

        Note that an overridden version of this method might return a
        list or generator instead of a Django queryset.

        """
        if self.dupable_word_model is None:
            return self.__class__.objects.none()
        qs = self.__class__.objects.filter(**kwargs)
        if self.pk is not None:
            qs = qs.exclude(pk=self.pk)
        parts = self.get_dupable_words(
            getattr(self, self.dupable_words_field))
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


class SimilarObjects(dd.VirtualTable):
    """Shows the other objects which are similar to this one."""
    # display_mode = 'html'
    display_mode = 'summary'
    master = dd.Model
    abstract = True

    # class Row:

    #     def __init__(self, master, other):
    #         self.master = master
    #         self.other = other

    #     def summary_row(self, ar):
    #         yield ar.obj2html(self.other)

    #     def __unicode__(self):
    #         return unicode(self.other)

    @classmethod
    def get_data_rows(self, ar):
        mi = ar.master_instance
        if mi is None:
            return

        for o in mi.find_similar_instances(4):
            # yield self.Row(mi, o)
            yield o

    @dd.displayfield(_("Similar record"))
    def similar_record(self, obj, ar):
        # return ar.obj2html(obj.other)
        return ar.obj2html(obj)

    @classmethod
    def get_table_summary(self, obj, ar):
        chunks = []
        for other in ar.spawn(self, master_instance=obj):
            chunks.append(ar.obj2html(other))
        if len(chunks):
            s = getattr(obj, obj.dupable_words_field)
            words = ', '.join(obj.get_dupable_words(s))
            chunks.append(_("Phonetic words: {0}").format(words))
            return E.p(*join_elems(chunks))
        return ''

