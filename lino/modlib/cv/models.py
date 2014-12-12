# -*- coding: UTF-8 -*-
# Copyright 2008-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
See :mod:`ml.cv`.

"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

import cgi
import datetime
ONE_DAY = datetime.timedelta(days=1)

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy as pgettext
from django.utils.encoding import force_unicode

from lino import dd, rt, mixins
from lino.utils.xmlgen.html import E
from lino.utils.htmlgen import UL
from lino.modlib.countries.models import CountryCity


from .mixins import (SectorFunction, PersonHistoryEntry,
                     HistoryByPerson, CefLevel, HowWell,
                     SchoolingStates)

config = dd.plugins.cv


## Language knowledge

class LanguageKnowledge(dd.Model):

    class Meta:
        verbose_name = _("language knowledge")
        verbose_name_plural = _("language knowledges")

    allow_cascaded_delete = ['person']

    person = models.ForeignKey(config.person_model)
    language = dd.ForeignKey("languages.Language")
    spoken = HowWell.field(_("Spoken"), blank=True)
    written = HowWell.field(_("Written"), blank=True)
    spoken_passively = HowWell.field(_("Spoken (passively)"),
                                     blank=True)
    written_passively = HowWell.field(_("Written (passively)"),
                                      blank=True)
    native = models.BooleanField(_("native language"), default=False)
    cef_level = CefLevel.field(blank=True)  # ,null=True)

    def __unicode__(self):
        if self.language_id is None:
            return ''
        if self.cef_level:
            return u"%s (%s)" % (self.language, self.cef_level)
        if self.spoken > '1' and self.written > '1':
            return _(u"%s (s/w)") % self.language
        elif self.spoken > '1':
            return _(u"%s (s)") % self.language
        elif self.written > '1':
            return _(u"%s (w)") % self.language
        else:
            return unicode(self.language)


class LanguageKnowledges(dd.Table):
    model = LanguageKnowledge
    required = dd.required(
        user_groups='coaching', user_level='manager')


class LanguageKnowledgesByPerson(LanguageKnowledges):
    master_key = 'person'
    #~ label = _("Language knowledge")
    #~ button_label = _("Languages")
    column_names = "language native spoken written cef_level"
    required = dd.required(user_groups='coaching')
    auto_fit_column_widths = True


class KnowledgesByLanguage(LanguageKnowledges):
    master_key = 'language'
    column_names = "person native spoken written cef_level"
    required = dd.required(user_groups='coaching')


## Trainings


class TrainingType(mixins.BabelNamed):

    class Meta:
        verbose_name = _("Training Type")
        verbose_name_plural = _("Training Types")


class TrainingTypes(dd.Table):
    required = dd.required(user_groups='integ', user_level='admin')
    model = 'cv.TrainingType'
    order_by = ["name"]
    detail_layout = """
    name id
    cv.TrainingsByType
    """


class Schooling(PersonHistoryEntry, CountryCity):
    # abstract base class for Training and Study
    class Meta:
        abstract = True

    language = dd.ForeignKey("languages.Language", blank=True, null=True)

    school = models.CharField(_("Establishment"), max_length=200, blank=True)

    state = SchoolingStates.field(blank=True)

    remarks = models.TextField(
        blank=True, null=True, verbose_name=_("Remarks"))


class Training(Schooling):

    class Meta:
        verbose_name = _("Training")
        verbose_name_plural = _("Trainings")

    type = models.ForeignKey('cv.TrainingType')

    content = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_("Training content"))

    certificates = models.CharField(
        max_length=200,
        blank=True,  # null=True,
        verbose_name=_("Certificates"))

    def __unicode__(self):
        return unicode(self.type)


class Trainings(dd.Table):

    required = dd.required(user_groups='integ', user_level='manager')
    model = 'cv.Training'
    order_by = "country city type".split()

    detail_layout = """
    person start_date end_date
    type state #success certificates
    school country city
    remarks
    """


class TrainingsByCountry(Trainings):
    required = dd.required(user_groups='integ')
    master_key = 'country'


class TrainingsByType(Trainings):
    required = dd.required(user_groups='integ')
    master_key = 'type'


class TrainingsByPerson(HistoryByPerson, Trainings):
    required = dd.required(user_groups='integ')
    column_names = 'type content start_date end_date \
    school country state certificates *'
    auto_fit_column_widths = True


##
## Studies
##

class EducationLevel(mixins.BabelNamed, mixins.Sequenced):

    class Meta:
        verbose_name = _("Education Level")
        verbose_name_plural = _("Education Levels")


class EducationLevels(dd.Table):
    required = dict(user_groups='integ', user_level='manager')
    model = 'cv.EducationLevel'
    column_names = 'name *'
    order_by = ['name']
    detail_layout = """
    name
    StudyTypesByLevel
    StudiesByLevel
    """


class StudyType(mixins.BabelNamed):

    class Meta:
        verbose_name = _("Study Type")
        verbose_name_plural = _("Study Types")

    education_level = dd.ForeignKey(
        'cv.EducationLevel',
        null=True, blank=True)


class StudyTypes(dd.Table):
    required = dd.required(user_groups='integ', user_level='admin')
    #~ label = _('Study types')
    model = StudyType
    order_by = ["name"]
    detail_layout = """
    name education_level id
    isip.ContractsByStudyType
    cv.StudiesByType
    """

    insert_layout = """
    name
    education_level
    """


class StudyTypesByLevel(StudyTypes):
    master_key = 'education_level'


class Study(Schooling):

    class Meta:
        verbose_name = _("Study")
        verbose_name_plural = _("Studies")

    type = models.ForeignKey('cv.StudyType')

    education_level = dd.ForeignKey(
        'cv.EducationLevel',
        null=True, blank=True)

    content = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_("Study content"))

    # success = models.BooleanField(verbose_name=_("Success"), default=False)

    def __unicode__(self):
        return unicode(self.type)


class Studies(dd.Table):

    "General list of Studies (all Persons)"
    required = dd.required(user_groups='integ', user_level='manager')
    model = 'cv.Study'
    order_by = "country city type content".split()

    detail_layout = """
    person start_date end_date
    type content education_level state #success
    school country city
    remarks
    """


class StudiesByCountry(Studies):
    required = dd.required(user_groups='integ')
    master_key = 'country'


class StudiesByLevel(Studies):
    required = dd.required(user_groups='integ')
    master_key = 'education_level'


class StudiesByPlace(Studies):

    """
    Lists all Studies in a given Place.
    Used as slave grid in Places detail.
    """
    required = dd.required(user_groups='integ')
    master_key = 'city'
    column_names = 'school type person content start_date end_date \
    state language remarks *'


class StudiesByType(Studies):
    required = dd.required(user_groups='integ')
    master_key = 'type'
    column_names = 'school person content start_date end_date \
    state language remarks *'


class StudiesByPerson(HistoryByPerson, Studies):
    required = dd.required(user_groups='integ')
    column_names = 'type content start_date end_date school country \
    state education_level *'
    auto_fit_column_widths = True


## Work Experiences


class Status(mixins.BabelNamed):

    class Meta:
        verbose_name = _("Status")
        verbose_name_plural = _('Statuses')


class Statuses(dd.Table):
    required = dd.required(user_groups='integ', user_level='manager')
    model = 'cv.Status'
    order_by = ['name']

    detail_layout = """
    id name
    ExperiencesByStatus
    """


class Regime(mixins.BabelNamed):
    # e.g. "38h/week"
    class Meta:
        verbose_name = _("Work Regime")
        verbose_name_plural = _('Work Regimes')


class Regimes(dd.Table):
    required = dd.required(user_groups='integ', user_level='manager')
    model = 'cv.Regime'
    order_by = ['name']
    detail_layout = """
    id name
    ExperiencesByRegime
    """


class Duration(mixins.BabelNamed):
    class Meta:
        verbose_name = _("Contract Duration")
        verbose_name_plural = _('Contract Durations')


class Durations(dd.Table):
    required = dd.required(user_groups='integ', user_level='manager')
    model = 'cv.Duration'
    order_by = ['name']
    detail_layout = """
    id name
    ExperiencesByDuration
    """


class Sector(mixins.BabelNamed):

    class Meta:
        verbose_name = _("Job Sector")
        verbose_name_plural = _('Job Sectors')

    remark = models.TextField(
        blank=True,
        verbose_name=_("Remark"))


class Sectors(dd.Table):
    required = dd.required(user_groups='integ', user_level='manager')
    model = Sector
    order_by = ['name']
    detail_layout = """
    id name
    remark FunctionsBySector
    cv.ExperiencesBySector
    jobs.CandidaturesBySector
    """


class Function(mixins.BabelNamed):

    """Each Job may have a Function."""
    class Meta:
        verbose_name = _("Job Function")
        verbose_name_plural = _('Job Functions')

    remark = models.TextField(
        blank=True,
        verbose_name=_("Remark"))

    sector = models.ForeignKey(Sector)
        #~ related_name="%(app_label)s_%(class)s_set_by_provider",
        #~ verbose_name=_("Job Provider"),
        #~ blank=True,null=True)


class Functions(dd.Table):
    #~ debug_permissions = 20130704
    required = dd.required(user_groups='integ', user_level='manager')
    model = 'cv.Function'
    column_names = 'name sector *'
    order_by = ['name']
    detail_layout = """
    id name sector
    remark
    jobs.CandidaturesByFunction
    cv.ExperiencesByFunction
    """


class FunctionsBySector(Functions):
    master_key = 'sector'


class Experience(PersonHistoryEntry, SectorFunction, CountryCity):

    class Meta:
        verbose_name = _("Job Experience")
        verbose_name_plural = _("Job Experiences")
        get_latest_by = 'start_date'

    company = models.CharField(max_length=200, verbose_name=_("company"))
    #~ type = models.ForeignKey(JobType,verbose_name=_("job type"))
    title = models.CharField(
        max_length=200, verbose_name=_("job title"), blank=True)
    status = dd.ForeignKey('cv.Status', blank=True, null=True)
    duration = dd.ForeignKey('cv.Duration', blank=True, null=True)
    regime = dd.ForeignKey('cv.Regime', blank=True, null=True)
    is_training = models.BooleanField(_("Training"), default=False)

    remarks = models.TextField(_("Remarks"), blank=True, null=True)

    termination_reason = models.CharField(
        max_length=200,
        blank=True,  # null=True,
        verbose_name=_("Termination reason"))

    def __unicode__(self):
        return unicode(self.title)


class Experiences(dd.Table):
    required = dd.required(user_groups='integ', user_level='manager')
    model = 'cv.Experience'
    # stay_in_grid = True
    detail_layout = """
    person start_date end_date termination_reason
    company country city
    sector function title
    status duration regime is_training
    remarks
    """


class ExperiencesBySector(Experiences):
    required = dd.required(user_groups='integ')
    master_key = 'sector'
    order_by = ["start_date"]


class ExperiencesByFunction(Experiences):
    required = dd.required(user_groups='integ')
    master_key = 'function'
    order_by = ["start_date"]


class ExperiencesByPerson(HistoryByPerson, Experiences):
    required = dd.required(user_groups='integ')
    auto_fit_column_widths = True
    column_names = "company start_date end_date function title \
    status duration country remarks *"


class ExperiencesByStatus(Experiences):
    master_key = 'status'
    column_names = "company start_date end_date title sector \
    function country remarks"


class ExperiencesByRegime(Experiences):
    master_key = 'regime'
    column_names = "company start_date end_date title sector \
    function country remarks"


class ExperiencesByDuration(Experiences):
    master_key = 'duration'
    column_names = "company start_date end_date title sector \
    function country remarks"


@dd.receiver(dd.post_analyze)
def set_detail_layouts(sender=None, **kwargs):
    rt.modules.languages.Languages.set_detail_layout("""
    id iso2 name
    cv.KnowledgesByLanguage
    """)


def setup_config_menu(site, ui, profile, m):
    m = m.add_menu(config.app_label, config.verbose_name)
    m.add_action('cv.TrainingTypes')
    m.add_action('cv.StudyTypes')
    m.add_action('cv.EducationLevels')
    m.add_action('cv.Sectors')
    m.add_action('cv.Functions')
    m.add_action('cv.Regimes')
    m.add_action('cv.Statuses')
    m.add_action('cv.Durations')


def setup_explorer_menu(site, ui, profile, m):
    m = m.add_menu(config.app_label, config.verbose_name)
    m.add_action('cv.LanguageKnowledges')
    m.add_action('cv.Trainings')
    m.add_action('cv.Studies')
    m.add_action('cv.Experiences')


