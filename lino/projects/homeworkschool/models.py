# Copyright 2012-2015 Luc Saffre
# License: BSD (see file COPYING for details)

from django.db import models
from django.utils.translation import ugettext_lazy as _


from lino.api import dd, rt
from lino import mixins
#~ from lino.models import SiteConfig

#~ from lino.modlib.contacts import models as contacts
#~ from lino.modlib.cal import models as cal

contacts = dd.resolve_app('contacts')
#~ cal = dd.resolve_app('cal')
#~ school = dd.resolve_app('school')


class School(contacts.Company):

    class Meta:
        #~ app_label = 'school'
        verbose_name = _("School")
        verbose_name_plural = _("Schools")


class Schools(contacts.Companies):
    model = School


class Person(contacts.Person, mixins.Born):

    class Meta(contacts.Person.Meta):
        app_label = 'contacts'
        # ~ # see :srcref:`docs/tickets/14`
        #~ verbose_name = _("Person")
        #~ verbose_name_plural = _("Persons")


class PersonDetail(contacts.PersonDetail):

    #~ contact = contacts.PersonDetail.main
    #~ outbox = dd.Panel("""
    #~ outbox.MailsByProject
    #~ """,label = _("Correspondence"))
    #~ calendar = dd.Panel("""
    #~ cal.EventsByProject
    #~ cal.TasksByProject
    #~ """,label = _("Calendar"))
    #~ main = "contact outbox calendar"
    main = """
    box1 box2
    remarks contacts.RolesByPerson households.MembersByPerson
    """

    box1 = """
    last_name first_name:15 #title:10
    country city zip_code:10
    #street_prefix street:25 street_no street_box
    addr2:40
    is_pupil is_teacher
    """

    box2 = """
    id:12 language
    email
    phone fax
    gsm
    gender birth_date age:10 
    """


    #~ def setup_handle(self,lh):

        #~ lh.contact.label = _("Contact")
        #~ lh.mails.label = _("Mails")


#~ class Company(contacts.Partner,contacts.CompanyMixin):
    #~ class Meta(contacts.CompanyMixin.Meta):
        #~ app_label = 'contacts'
        # ~ # see :srcref:`docs/tickets/14`
        #~ verbose_name = _("Company")
        #~ verbose_name_plural = _("Companies")
#~ class Event(cal.Event):
    #~ class Meta(cal.Event.Meta):
        #~ app_label = 'cal'
#~ class Task(cal.Task):
    #~ class Meta(cal.Task.Meta):
        #~ app_label = 'cal'
#~ class EventDetail(cal.EventDetail):
#~ class EventDetail(dd.FormLayout):
    #~ main = "general more"
    #~ lesson = dd.Panel("""
    #~ owner start_date start_time end_time place
    #~ school.PresencesByEvent
    #~ """,label=_("Lesson"))
    #~ event = dd.Panel("""
    # ~ id:8 user priority access_class transparent #rset
    #~ summary state workflow_buttons
    #~ calendar created:20 modified:20
    #~ description
    #~ cal.GuestsByEvent
    #~ """,label=_("Event"))
    #~ main = "lesson event"
    #~ def setup_handle(self,lh):
        #~ lh.lesson.label = _("Lesson")
        #~ lh.event.label =
        #~ lh.notes.label = _("Notes")

@dd.receiver(dd.post_analyze)
def my_details(sender, **kw):
    site = sender

    site.modules.cal.Events.set_detail_layout('general more')
    site.modules.cal.Events.add_detail_panel('general', """
    event_type summary user project 
    start end 
    room priority access_class transparent #rset 
    owner workflow_buttons
    description cal.GuestsByEvent 
    """, _("General"))

    site.modules.cal.Events.add_detail_panel('more', """
    id created:20 modified:20  
    outbox.MailsByController #postings.PostingsByController
    """, _("More"))

    # remove `project` field
    #~ site.modules.cal.Tasks.set_detail_layout("""
    #~ start_date workflow_buttons due_date done user id
    #~ summary
    #~ calendar owner created:20 modified:20 user_modified
    # ~ description #notes.NotesByTask
    #~ """)
    #~ site.modules.cal.Events.set_detail_layout("general more")
    site.modules.cal.Events.set_insert_layout("""
    summary 
    start end 
    event_type project 
    """,
                                              start="start_date start_time",
                                              end="end_date end_time",
                                              window_size=(60, 'auto'))


# TODO : move to plugin
def setup_main_menu(config, site, profile, main):
    m = main.get_item("contacts")
    m.add_action('homeworkschool.Schools')


def customize_school():
    dd.inject_field('courses.Pupil',
                    'school',
                    models.ForeignKey(School,
                                      blank=True, null=True,
            help_text=_("""The regular school where this child goes.""")
                    ))

customize_school()
