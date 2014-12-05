# -*- coding: UTF-8 -*-
# Copyright 2012-2014 Luc Saffre
# License: BSD (see file COPYING for details)

from __future__ import unicode_literals
from __future__ import print_function

"""
The :xfile:`models.py` module for the :mod:`lino.modlib.courses` app.

Models:

Slot
Topic
Line
Course
Enrolment

"""

import logging
logger = logging.getLogger(__name__)

from decimal import Decimal
ZERO = Decimal()
ONE = Decimal(1)

from django.db import models
from django.db.models import Q
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy as pgettext

from lino import dd, rt
from lino import mixins

from lino.utils import join_elems
from lino.utils.xmlgen.html import E
from lino.modlib.contacts.utils import parse_name


config = settings.SITE.plugins.courses

users = dd.resolve_app('users')
cal = dd.resolve_app('cal')
sales = dd.resolve_app('sales')
contacts = dd.resolve_app('contacts')

"""
Here we must use `resolve_model` with `strict=True`
because we want the concrete model
and we don't know whether it is overridden
by this application.
"""
Person = dd.resolve_model('contacts.Person', strict=True)
# equivalent alternative :
#~ Person = settings.SITE.modules.contacts.Person


class CourseAreas(dd.ChoiceList):
    verbose_name = _("Course area")
    verbose_name_plural = _("Course areas")
add = CourseAreas.add_item
add('C', _("Courses"), 'default')
# add('J', _("Journeys"), 'journeys')


class StartEndTime(dd.Model):

    class Meta:
        abstract = True
    start_time = models.TimeField(
        blank=True, null=True,
        verbose_name=_("Start Time"))
    end_time = models.TimeField(
        blank=True, null=True,
        verbose_name=_("End Time"))


class Slot(mixins.Sequenced, StartEndTime):

    """
    """
    class Meta:
        verbose_name = _("Timetable Slot")  # Zeitnische
        verbose_name_plural = _('Timetable Slots')

    name = models.CharField(max_length=200,
                            blank=True,
                            verbose_name=_("Name"))

    def __unicode__(self):
        return self.name or "%s-%s" % (self.start_time, self.end_time)


class Slots(dd.Table):
    model = Slot
    required = dd.required(user_level='manager')
    insert_layout = """
    start_time end_time
    name
    """
    detail_layout = """
    name start_time end_time
    courses.CoursesBySlot
    """


class Topic(mixins.BabelNamed, mixins.Printable):

    class Meta:
        verbose_name = _("Topic")
        verbose_name_plural = _('Topics')


class Topics(dd.Table):
    model = Topic
    required = dd.required(user_level='manager')
    detail_layout = """
    id name
    courses.LinesByTopic
    courses.CoursesByTopic
    """


class Line(mixins.BabelNamed):
    # a line (series) of courses. 
    class Meta:
        verbose_name = _("Course Line")
        verbose_name_plural = _('Course Lines')
        abstract = dd.is_abstract_model(__name__, 'Line')
    ref = dd.NullCharField(_("Reference"), max_length=30, unique=True)
    course_area = CourseAreas.field(blank=True)
    topic = models.ForeignKey(Topic, blank=True, null=True)
    description = dd.BabelTextField(_("Description"), blank=True)

    every_unit = cal.Recurrencies.field(
        _("Recurrency"),
        default=cal.Recurrencies.per_weekday,
        blank=True)  # iCal:DURATION
    every = models.IntegerField(_("Repeat every"), default=1)

    event_type = dd.ForeignKey(
        'cal.EventType', null=True, blank=True,
        help_text=_("""The Event Type to which events will be generated."""))

    tariff = dd.ForeignKey('products.Product',
                           blank=True, null=True,
                           verbose_name=_("Participation fee"),
                           related_name='lines_by_tariff')

    guest_role = dd.ForeignKey(
        "cal.GuestRole", blank=True, null=True,
        help_text=_("Default guest role for particpants of events."))

    options_cat = dd.ForeignKey(
        'products.ProductCat',
        verbose_name=_("Options category"),
        related_name="courses_lines_by_options_cat",
        blank=True, null=True)

    fees_cat = dd.ForeignKey(
        'products.ProductCat',
        verbose_name=_("Fees category"),
        related_name="courses_lines_by_fees_cat",
        blank=True, null=True)

    @dd.chooser()
    def tariff_choices(cls, fees_cat):
        if not fees_cat:
            return []
        Product = rt.modules.products.Product
        return Product.objects.filter(cat=fees_cat)

    def __unicode__(self):
        if self.ref:
            return self.ref
        return super(Line, self).__unicode__()


class Lines(dd.Table):
    model = 'courses.Line'
    # required = dd.required(user_level='manager')
    detail_layout = """
    id name ref
    topic fees_cat tariff options_cat
    event_type guest_role every_unit every
    description
    courses.CoursesByLine
    """
    insert_layout = dd.FormLayout("""
    name
    ref topic
    every_unit every event_type
    description
    """, window_size=(70, 16))


class LinesByTopic(Lines):
    master_key = "topic"


class EventsByTeacher(cal.Events):
    help_text = _("Shows events of courses of this teacher")
    master = config.teacher_model
    column_names = 'when_text:20 owner room state'
    # column_names = 'when_text:20 course__line room state'
    auto_fit_column_widths = True

    @classmethod
    def get_request_queryset(self, ar):
        teacher = ar.master_instance
        if teacher is None:
            return []
        if True:
            return []
        # TODO: build a list of courses, then show events by course
        qs = super(EventsByTeacher, self).get_request_queryset(ar)
        mycourses = rt.modules.Course.objects.filter(teacher=teacher)
        qs = qs.filter(course__in=teacher.course_set.all())
        return qs


class CourseStates(dd.Workflow):
    required = dd.required(user_level='admin')

add = CourseStates.add_item
add('10', _("Draft"), 'draft', editable=True)
add('20', _("Registered"), 'registered', editable=False)
# add('30', _("Started"), 'started', editable=False)
# add('40', _("Ended"), 'ended', editable=False)
# add('50', _("Cancelled"), 'cancelled', editable=True)

# #~ ACTIVE_COURSE_STATES = set((CourseStates.published,CourseStates.started))
# ACTIVE_COURSE_STATES = set((CourseStates.registered, CourseStates.started))


class EnrolmentStates(dd.Workflow):
    verbose_name_plural = _("Enrolment states")
    required = dd.required(user_level='admin')
    invoiceable = models.BooleanField(_("invoiceable"), default=True)
    uses_a_place = models.BooleanField(_("Uses a place"), default=True)

add = EnrolmentStates.add_item
add('10', _("Requested"), 'requested', invoiceable=False, uses_a_place=False)
add('20', _("Confirmed"), 'confirmed', invoiceable=True, uses_a_place=True)
add('30', _("Cancelled"), 'cancelled', invoiceable=False, uses_a_place=False)
# add('40', _("Certified"), 'certified', invoiceable=True, uses_a_place=True)
#~ add('40', _("Started"),'started')
#~ add('50', _("Success"),'success')
#~ add('60', _("Award"),'award')
#~ add('90', _("Abandoned"),'abandoned')


class Course(cal.Reservation):
    """A Course is a group of pupils that regularily meet with a given
    teacher in a given room to speak about a given subject.

    The subject of a course is expressed by the :class:`Line`.

    """

    FILL_EVENT_GUESTS = False

    class Meta:
        abstract = dd.is_abstract_model(__name__, 'Course')
        verbose_name = _("Course")
        verbose_name_plural = _('Courses')

    line = models.ForeignKey('courses.Line')
    teacher = models.ForeignKey(
        config.teacher_model,
        verbose_name=_("Instructor"),
        blank=True, null=True)
    #~ room = models.ForeignKey(Room,blank=True,null=True)
    slot = models.ForeignKey(Slot, blank=True, null=True)
    description = dd.BabelTextField(_("Description"), blank=True)
    remark = models.TextField(_("Remark"), blank=True)

    quick_search_fields = ('line__name', 'line__topic__name')

    state = CourseStates.field(default=CourseStates.draft)

    max_places = models.PositiveIntegerField(
        pgettext("in a course", "Places"),
        help_text=("Maximal number of participants"),
        blank=True, null=True)

    name = models.CharField(max_length=100,
                            blank=True,
                            verbose_name=_("Name"))
    tariff = dd.ForeignKey('products.Product',
                           blank=True, null=True,
                           verbose_name=_("Participation fee"),
                           related_name='courses_by_tariff')

    enrolments_until = models.DateField(
        _("Enrolments until"), blank=True, null=True)

    duplicate = mixins.Duplicate()

    def on_duplicate(self, ar, master):
        self.state = CourseStates.draft
        super(Course, self).on_duplicate(ar, master)

    @classmethod
    def get_registrable_fields(cls, site):
        for f in super(Course, cls).get_registrable_fields(site):
            yield f
        yield 'line'
        yield 'teacher'
        yield 'name'
        yield 'enrolments_until'
        yield 'tariff'

    def __unicode__(self):
        if self.name:
            return self.name
        if self.room is None:
            return "%s (%s)" % (self.line, dd.dtos(self.start_date))
        return u"%s (%s %s)" % (
            self.line,
            dd.dtos(self.start_date),
            self.room)

    @dd.chooser()
    def tariff_choices(cls, line):
        if not line or not line.fees_cat:
            return []
        Product = rt.modules.products.Product
        return Product.objects.filter(cat=line.fees_cat)

    def update_cal_from(self, ar):
        """Note: if recurrency is per_weekday, actual start may be
        later than self.start_date

        """
        # if self.state in (CourseStates.draft, CourseStates.cancelled):
        # if self.state == CourseStates.cancelled:
        #     ar.info("No start date because state is %s", self.state)
        #     return None
        return self.start_date

    def update_cal_calendar(self):
        return self.line.event_type

    def update_cal_summary(self, i):
        return "%s %s" % (dd.babelattr(
            self.line.event_type, 'event_label'), i)

    def suggest_cal_guests(self, event):
        # logger.info("20140314 suggest_guests")
        Guest = rt.modules.cal.Guest
        if self.line is None:
            return
        gr = self.line.guest_role
        if gr is None:
            return
        fkw = dict(course=self)
        states = (EnrolmentStates.requested, EnrolmentStates.confirmed)
        fkw.update(state__in=states)
        for obj in Enrolment.objects.filter(**fkw):
            yield Guest(
                event=event,
                partner=obj.pupil,
                role=gr)

    def get_free_places(self):
        used_states = EnrolmentStates.filter(uses_a_place=True)
        qs = Enrolment.objects.filter(course=self, state__in=used_states)
        res = qs.aggregate(models.Sum('places'))
        # logger.info("20140819 %s", res)
        used_places = res['places__sum'] or 0
        return self.max_places - used_places

    def full_clean(self, *args, **kw):
        if self.line_id is not None:
            if self.id is None:
                descs = dd.field2kw(self.line, 'description')
                descs = dd.babelkw('description', **descs)
                for k, v in descs.items():
                    setattr(self, k, v)
            if self.every_unit is None:
                self.every_unit = self.line.every_unit
            if self.every is None:
                self.every = self.line.every
        if self.enrolments_until is None:
            self.enrolments_until = self.start_date
        # if self.id is not None:
        #     if self.enrolments_until is None:
        #         qs = self.get_existing_auto_events()
        #         if qs.count():
        #             self.enrolments_until = qs[0].start_date
        super(Course, self).full_clean(*args, **kw)

    def before_auto_event_save(self, event):
        """
        Sets room and start_time for automatic events.
        This is a usage example for
        :meth:`EventGenerator.before_auto_event_save
        <lino.modlib.cal.models.EventGenerator.before_auto_event_save>`.
        """
        #~ logger.info("20131008 before_auto_event_save")
        assert not settings.SITE.loading_from_dump
        assert event.owner == self
        #~ event = instance
        if event.is_user_modified():
            return
        #~ if event.is_fixed_state(): return
        #~ course = event.owner
        #~ event.project = self
        event.course = self
        event.room = self.room
        if self.slot:
            event.start_time = self.slot.start_time
            event.end_time = self.slot.end_time
        else:
            event.start_time = self.start_time
            event.end_time = self.end_time

    @dd.displayfield(_("Info"))
    def info(self, ar):
        return unicode(self)

    #~ @dd.displayfield(_("Where"))
    #~ def where_text(self,ar):
        # ~ return unicode(self.room) # .company.city or self.company)

    @dd.displayfield(_("Events"))
    def events_text(self, ar=None):
        return ', '.join([
            config.day_and_month(e.start_date)
            for e in self.events_by_course.order_by('start_date')])

    @dd.displayfield(_("Available places"), max_length=5)
    def free_places(self, ar=None):
        if not self.max_places:
            return _("Unlimited")
        return str(self.get_free_places())

    @property
    def events_by_course(self):
        ct = dd.ContentType.objects.get_for_model(self.__class__)
        return cal.Event.objects.filter(owner_type=ct, owner_id=self.id)

    @dd.requestfield(_("Requested"))
    def requested(self, ar):
        return EnrolmentsByCourse.request(
            self, param_values=dict(state=EnrolmentStates.requested))

    @dd.requestfield(_("Confirmed"))
    def confirmed(self, ar):
        return EnrolmentsByCourse.request(
            self, param_values=dict(state=EnrolmentStates.confirmed))

    @dd.requestfield(_("Enrolments"))
    def enrolments(self, ar):
        return EnrolmentsByCourse.request(self)


# customize fields coming from mixins to override their inherited
# default verbose_names
dd.update_field(Course, 'every_unit', default=models.NOT_PROVIDED)
dd.update_field(Course, 'every', default=models.NOT_PROVIDED)


if Course.FILL_EVENT_GUESTS:

    @dd.receiver(dd.post_save, sender=cal.Event,
                 dispatch_uid="fill_event_guests_from_course")
    def fill_event_guests_from_course(sender=None, instance=None, **kw):
        #~ logger.info("20130528 fill_event_guests_from_course")
        if settings.SITE.loading_from_dump:
            return
        event = instance
        if event.is_user_modified():
            return
        if event.is_fixed_state():
            return
        if not isinstance(event.owner, Course):
            return
        course = event.owner
        if event.guest_set.count() > 0:
            return
        for e in course.enrolment_set.all():
            cal.Guest(partner=e.pupil, event=event).save()


class CourseDetail(dd.FormLayout):
    #~ start = "start_date start_time"
    #~ end = "end_date end_time"
    #~ freq = "every every_unit"
    #~ start end freq
    main = "general events courses.EnrolmentsByCourse"
    general = dd.Panel("""
    line teacher start_date end_date start_time end_time
    user room #slot workflow_buttons id:8
    description
    """, label=_("General"))
    events = dd.Panel("""
    max_places max_events max_date every_unit every
    monday tuesday wednesday thursday friday saturday sunday
    cal.EventsByController
    """, label=_("Events"))
    # enrolments = dd.Panel("""
    # OptionsByCourse:20 EnrolmentsByCourse:40
    # """, label=_("Enrolments"))


class Courses(dd.Table):
    model = 'courses.Course'
    #~ order_by = ['date','start_time']
    detail_layout = CourseDetail()
    insert_layout = """
    start_date
    line teacher
    """
    column_names = "start_date #info line teacher room workflow_buttons *"
    # order_by = ['start_date']
    # order_by = 'line__name room__name start_date'.split()
    order_by = ['name']
    auto_fit_column_widths = True

    parameters = dd.ObservedPeriod(
        line=models.ForeignKey('courses.Line', blank=True, null=True),
        topic=models.ForeignKey('courses.Topic', blank=True, null=True),
        city=models.ForeignKey('countries.Place', blank=True, null=True),
        teacher=models.ForeignKey(
            config.teacher_model,
            blank=True, null=True),
        user=models.ForeignKey(
            settings.SITE.user_model,
            blank=True, null=True),
        state=CourseStates.field(blank=True),
        active=mixins.YesNo.field(blank=True),
    )
    params_layout = """topic line city teacher user state active:10"""

    simple_param_fields = 'line teacher state user'.split()

    @classmethod
    def get_request_queryset(self, ar):
        qs = super(Courses, self).get_request_queryset(ar)
        if isinstance(qs, list):
            return qs
        for n in self.simple_param_fields:
            v = ar.param_values.get(n)
            if v:
                qs = qs.filter(**{n: v})
                #~ print(20130530, qs.query)

        if ar.param_values.topic:
            qs = qs.filter(line__topic=ar.param_values.topic)
        if ar.param_values.city:
            flt = Q(room__isnull=True)
            flt |= Q(room__company__city=ar.param_values.city)
            qs = qs.filter(flt)
        flt = Q(enrolments_until__isnull=True) | \
              Q(enrolments_until__gte=dd.today())
        if ar.param_values.active == mixins.YesNo.yes:
            qs = qs.filter(flt)
        elif ar.param_values.active == mixins.YesNo.no:
            qs = qs.exclude(flt)
        # logger.info("20140820 %s", dd.today())
        return qs

    @classmethod
    def get_title_tags(self, ar):
        for t in super(Courses, self).get_title_tags(ar):
            yield t

        if ar.param_values.city:
            yield _("in %s") % ar.param_values.city
        if ar.param_values.topic:
            yield unicode(ar.param_values.topic)
        for n in self.simple_param_fields:
            v = ar.param_values.get(n)
            if v:
                yield unicode(v)

    @dd.chooser()
    def city_choices(cls):
        Place = rt.modules.countries.Place
        Room = rt.modules.cal.Room
        places = set([
            obj.company.city.id
            for obj in Room.objects.filter(company__isnull=False)])
        # logger.info("20140822 city_choices %s", places)
        return Place.objects.filter(id__in=places)


class CoursesByTeacher(Courses):
    master_key = "teacher"
    column_names = "start_date start_time end_time line room *"
    order_by = ['start_date']


class CoursesByLine(Courses):
    master_key = "line"
    column_names = "info weekdays_text room times_text teacher *"
    order_by = ['room__name', 'start_date']

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(Courses, self).param_defaults(ar, **kw)
        kw.update(state=CourseStates.registered)
        kw.update(active=mixins.YesNo.yes)
        return kw


class CoursesByTopic(Courses):
    master = Topic
    order_by = ['start_date']
    column_names = "start_date:8 line:20 room:10 weekdays_text:10 times_text:10"

    @classmethod
    def get_request_queryset(self, ar):
        topic = ar.master_instance
        if topic is None:
            return []
        return settings.SITE.modules.courses.Course.objects.filter(
            line__topic=topic)


class CoursesBySlot(Courses):
    master_key = "slot"


class DraftCourses(Courses):
    label = _("Draft courses")
    column_names = 'info teacher room *'
    hide_sums = True

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(Courses, self).param_defaults(ar, **kw)
        kw.update(state=CourseStates.draft)
        kw.update(user=ar.get_user())
        # kw.update(active=mixins.YesNo.yes)
        return kw


class ActiveCourses(Courses):

    label = _("Active courses")
    #~ column_names = 'info requested confirmed teacher company room'
    column_names = 'info enrolments free_places teacher room *'
    #~ auto_fit_column_widths = True
    hide_sums = True

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(Courses, self).param_defaults(ar, **kw)
        kw.update(state=CourseStates.registered)
        kw.update(active=mixins.YesNo.yes)
        return kw

if False:

    class Option(mixins.BabelNamed):

        class Meta:
            abstract = dd.is_abstract_model(__name__, 'Option')
            verbose_name = _("Enrolment option")
            verbose_name_plural = _('Enrolment options')

        course = dd.ForeignKey('courses.Course')

        price = dd.ForeignKey('products.Product',
                              verbose_name=_("Price"),
                              null=True, blank=True)

    class Options(dd.Table):
        model = 'courses.Option'
        required = dd.required(user_level='manager')
        stay_in_grid = True
        column_names = 'name price *'
        auto_fit_column_widths = True
        insert_layout = """
        name
        price
        """
        detail_layout = """
        name
        id course price
        EnrolmentsByOption
        """

    class OptionsByCourse(Options):
        master_key = 'course'
        required = dd.required()


## ENROLMENT

class CreateInvoiceForEnrolment(sales.CreateInvoice):

    def get_partners(self, ar):
        return [o.pupil for o in ar.selected_rows]


class ConfirmedSubmitInsert(dd.SubmitInsert):
    def run_from_ui(self, ar, **kw):
        obj = ar.create_instance_from_request()
        msg = obj.get_confirm_veto(ar)
        if msg is None:
            obj.state = EnrolmentStates.confirmed
        self.save_new_instance(ar, obj)
        ar.set_response(close_window=True)


class Enrolment(mixins.UserAuthored, sales.Invoiceable):

    invoiceable_date_field = 'request_date'
    workflow_state_field = 'state'

    class Meta:
        abstract = dd.is_abstract_model(__name__, 'Enrolment')
        verbose_name = _("Enrolment")
        verbose_name_plural = _('Enrolments')
        unique_together = ('course', 'pupil')

    course_area = CourseAreas.field(blank=True)

    #~ teacher = models.ForeignKey(Teacher)
    course = dd.ForeignKey('courses.Course')
    pupil = dd.ForeignKey(config.pupil_model)
    request_date = models.DateField(
        _("Date of request"), default=dd.today)
    state = EnrolmentStates.field(default=EnrolmentStates.requested)
    amount = dd.PriceField(_("Participation fee"), blank=True)
    places = models.PositiveIntegerField(
        pgettext("in a course", "Places"),
        help_text=("number of participants"),
        default=1)
    option = dd.ForeignKey(
        'products.Product', verbose_name=_("Option"),
        blank=True, null=True)

    remark = models.CharField(_("Remark"), max_length=200, blank=True)
    confirmation_details = dd.RichTextField(
        _("Confirmation details"), blank=True,
        # format="html"
    )

    create_invoice = CreateInvoiceForEnrolment()
    submit_insert = ConfirmedSubmitInsert()

    @dd.chooser()
    def course_choices(cls, course_area):
        qs = rt.modules.courses.Course.objects.all()
        if course_area:
            qs = qs.filter(line__course_area=course_area)
        return qs

    @dd.chooser()
    def option_choices(cls, course):
        if not course.line or not course.line.options_cat:
            return []
        Product = rt.modules.products.Product
        return Product.objects.filter(cat=course.line.options_cat)

    @dd.chooser()
    def pupil_choices(cls, course):
        Pupil = dd.resolve_model(config.pupil_model)
        return Pupil.objects.all()

    def create_pupil_choice(self, text):
        """
        Called when an unknown pupil name was given.
        Try to auto-create it.
        """
        Pupil = dd.resolve_model(config.pupil_model)
        kw = parse_name(text)
        if len(kw) != 2:
            raise ValidationError(
                "Cannot find first and last names in %r to \
                auto-create pupil", text)
        p = Pupil(**kw)
        p.full_clean()
        p.save()
        return p

    def get_confirm_veto(self, ar):
        """
        Called from :class:`ml.courses.ConfirmEnrolment`.
        If this returns something else than None,
        then the enrolment won't be confirmed and the return value
        displayed to the user.
        """
        if self.course.max_places is None:
            return  # no veto. unlimited places.
        free = self.course.get_free_places()
        if free <= 0:
            return _("No places left in %s") % self.course
        #~ return _("Confirmation not implemented")

    def save(self, *args, **kw):
        if self.amount is None:
            self.compute_amount()
        super(Enrolment, self).save(*args, **kw)

    #~ def before_ui_save(self,ar):
        #~ if self.amount is None:
            #~ self.compute_amount()
        #~ super(Enrolment,self).before_ui_save(ar)

    def get_print_templates(self, bm, action):
        #~ if self.state:
        return [self.state.name + bm.template_ext]
        #~ return super(Enrolment,self).get_print_templates(bm,action)

    def __unicode__(self):
        return "%s / %s" % (self.course, self.pupil)

    def get_print_language(self):
        return self.pupil.language

    @classmethod
    def get_partner_filter(cls, partner):
        q1 = models.Q(pupil__invoice_recipient__isnull=True, pupil=partner)
        q2 = models.Q(pupil__invoice_recipient=partner)
        return models.Q(q1 | q2, invoice__isnull=True)

    def pupil_changed(self, ar):
        self.compute_amount()

    def compute_amount(self):
        #~ if self.course is None:
            #~ return
        tariff = self.get_invoiceable_product()
        # When `products` is not installed, then tariff may be None
        # because it is a DummyField.
        self.amount = getattr(tariff, 'sales_price', ZERO)

    def get_invoiceable_amount(self):
        return self.amount

    def get_invoiceable_product(self):
        #~ if self.course is not None:
        if self.state.invoiceable:
            return self.course.tariff or self.course.line.tariff

    def get_invoiceable_title(self):
        #~ if self.course is not None:
        return self.course

    def get_invoiceable_qty(self):
        return self.places


class Enrolments(dd.Table):
    #~ debug_permissions=20130531
    required = dd.required(user_level='manager')
    model = 'courses.Enrolment'
    stay_in_grid = True
    parameters = dd.ObservedPeriod(
        author=dd.ForeignKey(
            settings.SITE.user_model, blank=True, null=True),
        state=EnrolmentStates.field(blank=True, null=True),
        course_state=CourseStates.field(
            _("Course state"), blank=True, null=True),
        participants_only=models.BooleanField(
            _("Participants only"),
            help_text=_(
                "Hide cancelled enrolments. "
                "Ignored if you specify an explicit enrolment state."),
            default=True),
    )
    params_layout = """start_date end_date author state \
    course_state participants_only"""
    order_by = ['request_date']
    column_names = 'request_date course pupil workflow_buttons user *'
    #~ hidden_columns = 'id state'
    insert_layout = """
    request_date user
    course pupil
    remark
    """
    detail_layout = """
    request_date user
    course pupil
    remark amount workflow_buttons
    confirmation_details sales.InvoicingsByInvoiceable
    """

    @classmethod
    def get_request_queryset(self, ar):
        qs = super(Enrolments, self).get_request_queryset(ar)
        if isinstance(qs, list):
            return qs
        if ar.param_values.author is not None:
            qs = qs.filter(user=ar.param_values.author)

        if ar.param_values.state:
            qs = qs.filter(state=ar.param_values.state)
        else:
            if ar.param_values.participants_only:
                qs = qs.exclude(state=EnrolmentStates.cancelled)

        if ar.param_values.course_state:
            qs = qs.filter(course__state=ar.param_values.course_state)

        if ar.param_values.start_date is None or ar.param_values.end_date is None:
            period = None
        else:
            period = (ar.param_values.start_date, ar.param_values.end_date)
        if period is not None:
            qs = qs.filter(dd.inrange_filter('request_date', period))

        return qs

    @classmethod
    def get_title_tags(self, ar):
        for t in super(Enrolments, self).get_title_tags(ar):
            yield t

        if ar.param_values.state:
            yield unicode(ar.param_values.state)
        elif not ar.param_values.participants_only:
            yield unicode(_("Also ")) + unicode(EnrolmentStates.cancelled.text)
        if ar.param_values.course_state:
            yield unicode(
                settings.SITE.modules.courses.Course._meta.verbose_name) \
                + ' ' + unicode(ar.param_values.course_state)
        if ar.param_values.author:
            yield unicode(ar.param_values.author)


if dd.is_installed('products'):

    class EnrolmentsByOption(Enrolments):
        master_key = 'option'
        column_names = 'course pupil remark amount request_date *'
        order_by = ['request_date']
    

class ConfirmAllEnrolments(dd.Action):
    label = _("Confirm all")
    select_rows = False
    http_method = 'POST'

    def run_from_ui(self, ar, **kw):
        obj = ar.selected_rows[0]
        assert obj is None

        def ok(ar):
            for obj in ar:
                obj.state = EnrolmentStates.confirmed
                obj.save()
                ar.set_response(refresh_all=True)

        msg = _(
            "This will confirm all %d enrolments in this list.") % ar.get_total_count()
        ar.confirm(ok, msg, _("Are you sure?"))


class PendingRequestedEnrolments(Enrolments):

    label = _("Pending requested enrolments")
    auto_fit_column_widths = True
    params_panel_hidden = True
    column_names = 'request_date course pupil remark user amount workflow_buttons'
    hidden_columns = 'id state'

    # confirm_all = ConfirmAllEnrolments()

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(PendingRequestedEnrolments, self).param_defaults(ar, **kw)
        kw.update(state=EnrolmentStates.requested)
        return kw


class PendingConfirmedEnrolments(Enrolments):
    label = _("Pending confirmed enrolments")
    auto_fit_column_widths = True
    params_panel_hidden = True

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(PendingConfirmedEnrolments, self).param_defaults(ar, **kw)
        kw.update(state=EnrolmentStates.confirmed)
        # kw.update(course_state=CourseStates.ended)
        return kw


class EnrolmentsByPupil(Enrolments):
    params_panel_hidden = True
    required = dd.required()
    master_key = "pupil"
    column_names = 'request_date course user:10 remark amount:10 workflow_buttons *'
    auto_fit_column_widths = True
    _course_area = None  # CourseAreas.default

    @classmethod
    def get_known_values(self):
        if self._course_area is not None:
            return dict(course_area=self._course_area)
        return dict()

    @classmethod
    def get_actor_label(self):
        if self._course_area is not None:
            return self._course_area.text
        return _("Enrolments")

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(EnrolmentsByPupil, self).param_defaults(ar, **kw)
        kw.update(participants_only=False)
        return kw

    insert_layout = """
    course
    places option
    remark
    request_date user
    """


class EnrolmentsByCourse(Enrolments):
    params_panel_hidden = True
    required = dd.required()
    master_key = "course"
    column_names = 'request_date pupil_info option \
    remark amount:10 workflow_buttons *'
    auto_fit_column_widths = True
    # cell_edit = False

    insert_layout = """
    pupil
    places option
    remark
    request_date user
    """

    @dd.virtualfield(dd.HtmlBox(_("Participant")))
    def pupil_info(cls, self, ar):
        elems = [ar.obj2html(self.pupil,
                             self.pupil.get_full_name(nominative=True))]
        elems += [', ']
        elems += join_elems(
            list(self.pupil.address_location_lines()),
            sep=', ')
        return E.div(*elems)


# class EventsByCourse(cal.Events):
#     required = dd.required(user_groups='office')
#     master_key = 'course'
#     column_names = 'when_text:20 linked_date summary workflow_buttons *'
#     auto_fit_column_widths = True


# dd.inject_field(
#     'cal.Event',
#     'course',
#     dd.ForeignKey(
#         'courses.Course',
#         blank=True, null=True,
#         help_text=_("Fill in only if this event is a session of a course."),
#         related_name="events_by_course"))


class SuggestedCoursesByPupil(ActiveCourses):
    label = _("Suggested courses")
    column_names = 'info enrolments free_places custom_actions *'
    auto_fit_column_widths = True
    hide_sums = True
    master = config.pupil_model
    details_of_master_template = _("%(details)s for %(master)s")
    params_layout = 'topic line city teacher active'

    @classmethod
    def get_request_queryset(self, ar):
        qs = super(SuggestedCoursesByPupil, self).get_request_queryset(ar)
        pupil = ar.master_instance
        if pupil is not None:
            qs = qs.exclude(enrolment__pupil=pupil)
        return qs

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(SuggestedCoursesByPupil, self).param_defaults(ar, **kw)
        # kw.update(active=mixins.YesNo.yes)
        pupil = ar.master_instance
        if pupil and pupil.city:
            kw.update(city=pupil.city)
        return kw

    @dd.displayfield(_("Actions"))
    def custom_actions(self, course, ar, **kw):
        mi = ar.master_instance
        if mi is None:
            return ''
        kv = dict(course=course)
        # kv.update(granting=self)
        # at = self.aid_type
        # ct = at.confirmation_type
        # if not ct:
        #     return ''
        # free = course.get_free_places()
        sar = ar.spawn(EnrolmentsByPupil,
                       master_instance=mi, known_values=kv)
        if sar.get_total_count() == 0:
            txt = _("Enrol")
            btn = sar.insert_button(txt, icon_name=None)
        else:
            txt = _("Show enrolment")
            btn = ar.obj2html(sar.data_iterator[0])
        return E.div(btn)


def setup_main_menu(site, ui, profile, main):
    m = main.add_menu("courses", config.verbose_name)
    m.add_action('courses.Courses')
    m.add_action('courses.Lines')
    m.add_action('courses.PendingRequestedEnrolments')
    m.add_action('courses.PendingConfirmedEnrolments')


def setup_config_menu(site, ui, profile, m):
    m = m.add_menu("courses", config.verbose_name)
    #~ m.add_action(Rooms)
    m.add_action('courses.Topics')
    m.add_action('courses.Slots')


def setup_explorer_menu(site, ui, profile, m):
    m = m.add_menu("courses", config.verbose_name)
    #~ m.add_action(Presences)
    #~ m.add_action(Events)
    m.add_action('courses.Enrolments')
    # m.add_action('courses.Options')
    m.add_action('courses.EnrolmentStates')

dd.add_user_group('courses', config.verbose_name)
