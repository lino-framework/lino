# -*- coding: UTF-8 -*-
# Copyright 2009-2014 Luc Saffre
# License: BSD (see file COPYING for details)
"""
The :xfile:`models.py` file for :mod:`lino.modlib.notes`.
"""

import logging
logger = logging.getLogger(__name__)

import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy

from lino import dd
from lino import mixins
from django.conf import settings

from lino.modlib.postings.mixins import Postable
from lino.modlib.contenttypes.mixins import Controllable

outbox = dd.resolve_app('outbox')
contacts = dd.resolve_app('contacts')


class NoteType(mixins.BabelNamed, mixins.PrintableType, outbox.MailableType):

    templates_group = 'notes/Note'

    class Meta:
        verbose_name = _("Note Type")
        verbose_name_plural = _("Note Types")

    #~ name = models.CharField(max_length=200)
    important = models.BooleanField(
        verbose_name=_("important"),
        default=False)
    remark = models.TextField(verbose_name=_("Remark"), blank=True)


class NoteTypes(dd.Table):

    """
    Displays all rows of :class:`NoteType`.
    """
    model = 'notes.NoteType'
    required = dd.required(user_level='admin', user_groups='office')
    #~ label = _("Note types")
    column_names = 'name build_method template *'
    order_by = ["name"]

    insert_layout = """
    name
    build_method
    """

    detail_layout = """
    id name
    build_method template email_template attach_to_email
    remark:60x5
    notes.NotesByType
    """


class EventType(mixins.BabelNamed):

    """
    A possible choice for :attr:`Note.event_type`.
    """
    class Meta:
        verbose_name = pgettext_lazy(u"notes", u"Event Type")
        #~ verbose_name = _("Event Type")
        verbose_name_plural = _("Event Types")
    #~ name = dd.BabelCharField(max_length=200,verbose_name=_("Designation"))
    remark = models.TextField(verbose_name=_("Remark"), blank=True)
    body = dd.BabelTextField(_("Body"), blank=True, format='html')


class EventTypes(dd.Table):

    """
    List of all Event Types.
    """
    model = 'notes.EventType'
    required = dd.required(user_level='admin', user_groups='office')
    column_names = 'name *'
    order_by = ["name"]

    detail_layout = """
    id name
    remark:60x3
    notes.NotesByEventType:60x6
    """


class Note(mixins.TypedPrintable,
           mixins.UserAuthored,
           Controllable,
           contacts.ContactRelated,
           mixins.ProjectRelated,
           outbox.Mailable,
           Postable,
           ):

    """
    Deserves more documentation.
    """

    manager_level_field = 'office_level'

    class Meta:
        abstract = dd.is_abstract_model(__name__, 'Note')
        verbose_name = _("Note")
        verbose_name_plural = _("Notes")

    date = models.DateField(
        verbose_name=_('Date'), default=settings.SITE.today)
    time = models.TimeField(
        blank=True, null=True,
        verbose_name=_("Time"),
        default=datetime.datetime.now)
    type = models.ForeignKey(
        NoteType,
        blank=True, null=True,
        verbose_name=_('Note Type (Content)'))
    event_type = models.ForeignKey(
        EventType,
        blank=True, null=True,
        verbose_name=_('Event Type (Form)'))
    subject = models.CharField(_("Subject"), max_length=200, blank=True)
    body = dd.RichTextField(_("Body"), blank=True, format='html')

    language = dd.LanguageField()

    def __unicode__(self):
        return u'%s #%s' % (self._meta.verbose_name, self.pk)

    def summary_row(self, ar, **kw):
        #~ s = super(Note,self).summary_row(ui,rr)
        s = super(Note, self).summary_row(ar)
        #~ s = contacts.ContactDocument.summary_row(self,ui,rr)
        if self.subject:
            s += [' ', self.subject]
        return s

    #~ def update_owned_instance(self,task):
        #~ mixins.AutoUser.update_owned_instance(self,task)
        #~ contacts.PartnerDocument.update_owned_instance(self,task)
        #~ super(ContractBase,self).update_owned_instance(other)

    def get_mailable_type(self):
        return self.type

    #~ def get_person(self):
        #~ return self.project
    #~ person = property(get_person)

    def get_print_language(self):
        return self.language


dd.update_field(Note, 'company', verbose_name=_("Recipient (Organization)"))
dd.update_field(Note, 'contact_person', verbose_name=_("Recipient (Person)"))


def html_text(s):
    return '<div class="htmlText">' + s + '</div>'


class NoteDetail(dd.FormLayout):
    main = """
    date:10 time event_type:25 type:25
    subject project
    company contact_person contact_role
    id user:10 language:8 build_time
    body outbox.MailsByController
    """


class Notes(dd.Table):
    required = dd.required(user_groups='office', user_level='admin')

    model = 'notes.Note'
    detail_layout = NoteDetail()
    column_names = "date time id user event_type type project subject * body"
    order_by = ["date", "time"]


class MyNotes(mixins.ByUser, Notes):
    required = dd.required(user_groups='office')
    column_names = "date time event_type type subject project body *"
    order_by = ["date", "time"]


class NotesByType(Notes):
    master_key = 'type'
    column_names = "date time event_type subject user *"
    order_by = ["date", "time"]


class NotesByEventType(Notes):
    master_key = 'event_type'
    column_names = "date time type subject user *"
    order_by = ["date", "time"]


class NotesByX(Notes):
    required = dd.required(user_groups='office')
    column_names = "date time event_type type subject user *"
    order_by = ["-date", "-time"]

if settings.SITE.project_model is not None:

    class NotesByProject(NotesByX):
        master_key = 'project'


class NotesByOwner(NotesByX):
    master_key = 'owner'
    column_names = "date time event_type type subject user *"


class NotesByCompany(NotesByX):
    master_key = 'company'
    column_names = "date time event_type type subject user *"


class NotesByPerson(NotesByX):
    master_key = 'contact_person'
    column_names = "date time event_type type subject user *"


def add_system_note(ar, owner, subject, body, **kw):
    #~ if not settings.SITE.site_config.system_note_type:
        #~ return
    nt = owner.get_system_note_type(ar)
    if not nt:
        return
    prj = owner.get_related_project(ar)
    if prj:
        kw.update(project=prj)
    #~ note = Note(type=nt,owner=owner,
    note = Note(event_type=nt, owner=owner,
                subject=subject, body=body, user=ar.get_user(), **kw)
    #~ owner.update_system_note(note)
    note.save()


system = dd.resolve_app('system')


def customize_siteconfig():
    """
    Injects application-specific fields to :class:`SiteConfig <lino.modlib.system.SiteConfig>`.
    """
    dd.inject_field('system.SiteConfig',
                    'system_note_type',
                    #~ models.ForeignKey(NoteType,
                    models.ForeignKey(EventType,
                                      blank=True, null=True,
                                      verbose_name=_(
                                          "Default system note type"),
            help_text=_("""\
Note Type used by system notes.
If this is empty, then system notes won't create any entry to the Notes table.""")))


def setup_main_menu(site, ui, profile, m):
    m = m.add_menu("office", system.OFFICE_MODULE_LABEL)
    m.add_action('notes.MyNotes')


def setup_config_menu(site, ui, profile, m):
    #~ m  = m.add_menu("notes",_("~Notes"))
    m = m.add_menu("office", system.OFFICE_MODULE_LABEL)
    m.add_action('notes.NoteTypes')
    m.add_action('notes.EventTypes')


def setup_explorer_menu(site, ui, profile, m):
    m = m.add_menu("office", system.OFFICE_MODULE_LABEL)
    m.add_action('notes.Notes')

customize_siteconfig()
