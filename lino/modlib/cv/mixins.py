# -*- coding: UTF-8 -*-
# Copyright 2013-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
See :mod:`ml.cv`.
"""
from builtins import object

from django.db import models
from django.utils.translation import ugettext_lazy as _

from lino.api import dd, rt

from lino.mixins.periods import DatePeriod


class EducationEntryStates(dd.ChoiceList):
    """The possible states of an **education entry**.

    """
    verbose_name = _("State")

add = EducationEntryStates.add_item
add('0', _("Success"), 'success')
add('1', _("Failure"), 'failure')
add('2', _("Ongoing"), 'ongoing')


class HowWell(dd.ChoiceList):

    """A list of possible answers to questions of type "How well ...?":
    "not at all", "a bit", "moderate", "quite well" and "very well"
    
    which are stored in the database as '0' to '4',
    and whose `__str__()` returns their translated text.

    """
    verbose_name = _("How well?")

add = HowWell.add_item
add('0', _("not at all"))
add('1', _("a bit"))
add('2', _("moderate"), "default")
add('3', _("quite well"))
add('4', _("very well"))


class CefLevel(dd.ChoiceList):

    """
    Levels of the Common European Framework (CEF).
    
    | http://www.coe.int/t/dg4/linguistic/CADRE_EN.asp
    | http://www.coe.int/t/dg4/linguistic/Source/ManualRevision-proofread-FINAL_en.pdf
    | http://www.telc.net/en/what-telc-offers/cef-levels/a2/
    
    """
    verbose_name = _("CEF level")
    verbose_name_plural = _("CEF levels")
    show_values = True

    #~ @classmethod
    #~ def display_text(cls,bc):
        #~ def fn(bc):
            #~ return u"%s (%s)" % (bc.value,unicode(bc))
        #~ return lazy(fn,unicode)(bc)

add = CefLevel.add_item
add('A1', _("basic language skills"))
add('A2', _("basic language skills"))
add('A2+', _("basic language skills"))
add('B1', _("independent use of language"))
add('B2', _("independent use of language"))
add('B2+', _("independent use of language"))
add('C1', _("proficient use of language"))
add('C2', _("proficient use of language"))
add('C2+', _("proficient use of language"))


class SectorFunction(dd.Model):

    """
    Abstract base for models that refer to a
    :class:`Sector` and a :class:`Function`.
    """
    class Meta(object):
        abstract = True

    sector = dd.ForeignKey("cv.Sector", blank=True, null=True)
    function = dd.ForeignKey("cv.Function", blank=True, null=True)

    @dd.chooser()
    def function_choices(cls, sector):
        if sector is None:
            return rt.modules.cv.Function.objects.all()
        return sector.function_set.all()


class PersonHistoryEntry(DatePeriod):
    "Base class for Study, Experience"
    class Meta(object):
        abstract = True

    person = models.ForeignKey(dd.plugins.cv.person_model)


class HistoryByPerson(dd.Table):
    """Abstract base class for :class:`StudiesByPerson` and
    :class:`ExperiencesByPerson`

    """
    master_key = 'person'
    order_by = ["start_date"]

    @classmethod
    def create_instance(self, req, **kw):
        obj = super(HistoryByPerson, self).create_instance(req, **kw)
        if obj.person_id is not None:
            previous_exps = self.model.objects.filter(
                person=obj.person).order_by('start_date')
            if previous_exps.count() > 0:
                exp = previous_exps[previous_exps.count() - 1]
                if exp.end_date:
                    obj.start_date = exp.end_date
                else:
                    obj.start_date = exp.start_date
        return obj


