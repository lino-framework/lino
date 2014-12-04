# -*- coding: UTF-8 -*-
# Copyright 2013-2014 Luc Saffre
# License: BSD (see file COPYING for details)
"""The :xfile:`models` module for :mod:`lino.modlib.polls`.

"""

import logging
logger = logging.getLogger(__name__)

from django.db import models
from django.utils.translation import ugettext_lazy as _

from lino import dd, mixins
from lino.utils import join_elems

from lino.utils.xmlgen.html import E

from lino.mixins import Referrable

config = dd.plugins.polls

#~ def NullBooleanField(*args,**kw):
    #~ kw.setdefault('default', False)
    #~ return models.BooleanField(*args,**kw)
# ~ # not yet implemented:
NullBooleanField = models.NullBooleanField


class PollStates(dd.Workflow):

    """
    State of a Calendar Task. Used as Workflow selector.
    """
    verbose_name_plural = _("Poll States")
    required = dd.required(user_level='admin')


add = PollStates.add_item
add('10', _("Draft"), 'draft')
add('20', _("Published"), 'published')
add('30', _("Closed"), 'closed')


class ResponseStates(dd.Workflow):

    """
    Possible states of a Response.
    """
    verbose_name_plural = _("Response States")
    required = dd.required(user_level='admin')


add = ResponseStates.add_item
add('10', _("Draft"), 'draft', editable=True)
add('20', _("Registered"), 'registered', editable=False)


ResponseStates.registered.add_transition(_("Register"), states='draft')
ResponseStates.draft.add_transition(_("Deregister"), states="registered")


#~ class QuestionTypes(dd.ChoiceList):
    #~ verbose_name_plural = _("Question Types")
    #~ required = dd.required(user_level='admin')
    #~
#~ add = QuestionTypes.add_item
#~ add('10', _("Draft"),'draft',editable=True)


class ChoiceSet(mixins.BabelNamed):

    class Meta:
        verbose_name = _("Choice Set")
        verbose_name_plural = _("Choice Sets")


class ChoiceSets(dd.Table):
    model = ChoiceSet
    detail_layout = """
    name
    ChoicesBySet
    """


class Choice(mixins.BabelNamed, mixins.Sequenced):

    class Meta:
        verbose_name = _("Choice")
        verbose_name_plural = _("Choices")

    choiceset = models.ForeignKey('polls.ChoiceSet', related_name='choices')

    def get_siblings(self):
        return self.choiceset.choices.order_by('seqno')

    @dd.action()
    def select_by_response(self, ar):
        mi = ar.master_instance
        dd.logger.info("20140929 %s", mi)
        if isinstance(mi, Response):
            AnswerChoice(response=mi, choice=self).save()


class Choices(dd.Table):
    model = 'polls.Choice'


class ChoicesBySet(Choices):
    master_key = 'choiceset'


class Poll(mixins.UserAuthored, mixins.CreatedModified, Referrable):

    class Meta:
        abstract = dd.is_abstract_model(__name__, 'Poll')
        verbose_name = _("Poll")
        verbose_name_plural = _("Polls")
        ordering = ['created']

    title = models.CharField(_("Title"), max_length=200)

    details = models.TextField(_("Details"), blank=True)

    default_choiceset = models.ForeignKey(
        'polls.ChoiceSet',
        null=True, blank=True,
        related_name='polls',
        verbose_name=_("Default Choiceset"))

    default_multiple_choices = models.BooleanField(
        _("Allow multiple choices"), default=False)

    questions_to_add = models.TextField(
        _("Questions to add"),
        help_text=_("Paste text for questions to add. "
                    "Every non-empty line will create one question."),
        blank=True)

    state = PollStates.field(default=PollStates.draft)

    def __unicode__(self):
        return self.ref or self.title

    def after_ui_save(self, ar):
        if self.questions_to_add:
            #~ print "20131106 self.questions_to_add", self.questions_to_add
            #~ qkw = dict(choiceset=self.default_choiceset)
            qkw = dict()
            for ln in self.questions_to_add.splitlines():
                ln = ln.strip()
                if ln:
                    q = Question(poll=self, text=ln, **qkw)
                    q.full_clean()
                    q.save()
                    qkw.setdefault('seqno', q.seqno + 1)
            self.questions_to_add = ''
            self.save()  # save again because we modified afterwards

        super(Poll, self).after_ui_save(ar)

    @dd.virtualfield(dd.HtmlBox(_("Result")))
    def result(self, ar):
        return E.div(*tuple(get_poll_result(self)))


def get_poll_result(self):
    #~ yield E.h1(self.title)
    for cs in ChoiceSet.objects.all():
        questions = self.questions.filter(choiceset=cs)
        if questions.count() > 0:
            yield E.h2(unicode(cs))
            for question in questions:
                yield E.p(question.text)


class PollDetail(dd.FormLayout):
    main = "general results"

    general = dd.Panel("""
    title state
    details
    user created modified default_choiceset default_multiple_choices
    polls.QuestionsByPoll
    """, label=_("General"))

    results = dd.Panel("""
    polls.ResponsesByPoll
    # result
    PollResult
    """, label=_("Results"))


class Polls(dd.Table):
    model = 'polls.Poll'
    column_names = 'created title user state *'
    detail_layout = PollDetail()
    insert_layout = dd.FormLayout("""
    title
    default_choiceset default_multiple_choices
    questions_to_add
    """, window_size=(60, 15))


class MyPolls(mixins.ByUser, Polls):
    column_names = 'created title state *'


class Question(mixins.Sequenced):

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")

    poll = models.ForeignKey('polls.Poll', related_name='questions')
    text = models.TextField(verbose_name=_("Text"))
    choiceset = models.ForeignKey('polls.ChoiceSet', blank=True, null=True)
    multiple_choices = models.BooleanField(
        _("Allow multiple choices"), blank=True)

    def __unicode__(self):
        #~ return self.text[:40].strip() + ' ...'
        return self.text

    def get_siblings(self):
        #~ return self.choiceset.choices.order_by('seqno')
        return self.poll.questions.order_by('seqno')

    def get_choiceset(self):
        if self.choiceset is None:
            return self.poll.default_choiceset
        return self.choiceset

    def full_clean(self, *args, **kw):
        if self.multiple_choices is None:
            self.multiple_choices = self.poll.default_multiple_choices
        #~ if self.choiceset_id is None:
            #~ self.choiceset = self.poll.default_choiceset
        super(Question, self).full_clean()


class Questions(dd.Table):
    model = 'polls.Question'


class QuestionsByPoll(Questions):
    master_key = 'poll'
    column_names = 'text choiceset multiple_choices'
    auto_fit_column_widths = True


class ToggleChoice(dd.Action):
    parameters = dict(
        # response=dd.ForeignKey("polls.Response"),
        question=dd.ForeignKey("polls.Question"),
        choice=dd.ForeignKey("polls.Choice"),
    )
    no_params_window = True

    def run_from_ui(self, ar, **kw):
        response = ar.selected_rows[0]
        if response is None:
            return
        pv = ar.action_param_values
        try:
            obj = AnswerChoice.objects.get(response=response, **pv)
            obj.delete()
        except AnswerChoice.DoesNotExist:
            if not pv.question.multiple_choices:
                # delete any other choice which might exist
                qs = AnswerChoice.objects.filter(
                    response=response, question=pv.question)
                qs.delete()
            obj = AnswerChoice(response=response, **pv)
            obj.full_clean()
            obj.save()
        ar.success(refresh=True)
        # dd.logger.info("20140930 %s", obj)
            

class Response(mixins.UserAuthored, mixins.Registrable, mixins.CreatedModified):

    class Meta:
        verbose_name = _("Response")
        verbose_name_plural = _("Responses")
        ordering = ['created']

    poll = dd.ForeignKey('polls.Poll', related_name='responses')
    state = ResponseStates.field(default=ResponseStates.draft)
    remark = models.TextField(verbose_name=_("My general remark"), blank=True)
    partner = dd.ForeignKey('contacts.Partner', blank=True, null=True)

    toggle_choice = ToggleChoice()

    @dd.chooser()
    def poll_choices(cls):
        return Poll.objects.filter(state=PollStates.published)

    #~ def after_ui_save(self,ar):
        #~ if self.answers.count() == 0:
            #~ for obj in self.poll.questions.all():
                #~ Answer(response=self,question=obj).save()
                    #~
        #~ super(Response,self).after_ui_save(ar)

    def __unicode__(self):
        return _("%(user)s's response to %(poll)s") % dict(
            user=self.user, poll=self.poll)


class Responses(dd.Table):
    model = 'polls.Response'
    detail_layout = """
    user poll state created modified
    polls.AnswersByResponse
    remark
    """
    insert_layout = """
    user
    poll
    """

    @classmethod
    def get_detail_title(self, ar, obj):
        txt = _("response to %(poll)s") % dict(poll=obj.poll)
        if obj.user == ar.get_user():
            return _("My %s") % txt
        return _("%(user)s's %(what)s") % dict(user=obj.user, what=txt)


class MyResponses(mixins.ByUser, Responses):
    column_names = 'created poll state remark *'


class ResponsesByPoll(Responses):
    master_key = 'poll'
    column_names = 'created user state partner remark *'


class ResponsesByPartner(Responses):
    master_key = 'partner'
    column_names = 'created user state remark *'
    slave_grid_format = 'summary'

    @classmethod
    def get_slave_summary(self, obj, ar):
        if obj is None:
            return
        qs = Response.objects.filter(partner=obj).order_by(
            'poll__ref', 'modified')
        polls_with_responses = []
        current = None
        for resp in qs:
            if current is None:
                current = (resp.poll, [])
            if resp.poll != current[0]:
                polls_with_responses.append(current)
                current = (resp.poll, [])
            current[1].append(resp)
        if current is not None:
            polls_with_responses.append(current)
            
        items = []
        for poll, responses in polls_with_responses:
            elems = [unicode(poll), ' : ']
            elems += join_elems(
                [ar.obj2html(r, dd.fds(r.modified))
                 for r in responses], sep=', ')
            items.append(E.li(*elems))
        return E.div(E.ul(*items))


class AnswerChoice(dd.Model):

    class Meta:
        verbose_name = _("Answer Choice")
        verbose_name_plural = _("Answer Choices")
        ordering = ['question__seqno']

    response = models.ForeignKey('polls.Response')
    question = models.ForeignKey('polls.Question')
    choice = models.ForeignKey(
        'polls.Choice',
        related_name='answers', verbose_name=_("My answer"),
        blank=True, null=True)

    @dd.chooser()
    def choice_choices(cls, question):
        return question.get_choiceset().choices.all()


class AnswerChoices(dd.Table):
    model = 'polls.AnswerChoice'


class AnswerRemark(dd.Model):

    class Meta:
        verbose_name = _("Answer Remark")
        verbose_name_plural = _("Answer Remarks")
        ordering = ['question__seqno']

    response = models.ForeignKey('polls.Response')
    question = models.ForeignKey('polls.Question')
    remark = models.TextField(_("My remark"), blank=True)


class AnswerRemarks(dd.Table):
    model = 'polls.AnswerRemarks'

FORWARD_TO_QUESTION = tuple("full_clean after_ui_save disable_delete".split())


class Answer(object):
    """Volatile object to represent the one and only answer to a given
    question in a given response.

    """

    def __init__(self, response, question):
        self.response = response
        self.question = question
        self.pk = self.id = question.pk
        try:
            self.remark = AnswerRemark.objects.get(
                question=question, response=response)
        except AnswerRemark.DoesNotExist:
            self.remark = AnswerRemark(question=question, response=response)

        self.choices = AnswerChoice.objects.filter(
            question=question, response=response)
        for k in FORWARD_TO_QUESTION:
            setattr(self, k, getattr(question, k))


class AnswerRemarkField(dd.VirtualField):

    """
    An editable virtual field.
    """
    editable = True

    def __init__(self):
        t = models.TextField(_("My remark"), blank=True)
        dd.VirtualField.__init__(self, t, None)

    def set_value_in_object(self, ar, obj, value):
        #~ e = self.get_entry_from_answer(obj)
        obj.remark.remark = value
        obj.remark.save()

    def value_from_object(self, obj, ar):
        #~ logger.info("20120118 value_from_object() %s",dd.obj2str(obj))
        #~ e = self.get_entry_from_answer(obj)
        return obj.remark.remark


class AnswersByResponse(dd.VirtualTable):
    label = _("Answers")
    editable = True
    master = 'polls.Response'
    column_names = 'question:40 answer_buttons:30 remark:20 *'
    variable_row_height = True
    auto_fit_column_widths = True
    #~ slave_grid_format = 'html'

    remark = AnswerRemarkField()

    @classmethod
    def get_pk_field(self):
        return Question._meta.pk
        #~ return AnswerPKField()

    @classmethod
    def get_row_by_pk(self, ar, pk):
        response = ar.master_instance
        #~ if response is None: return
        q = Question.objects.get(pk=pk)
        return Answer(response, q)

    @classmethod
    def get_row_permission(cls, obj, ar, state, ba):
        return True

    @classmethod
    def disable_delete(self, obj, ar):
        return "Not deletable"

    @classmethod
    def get_data_rows(self, ar):
        response = ar.master_instance
        if response is None:
            return
        for q in Question.objects.filter(poll=response.poll):
            yield Answer(response, q)

    @dd.displayfield(_("Question"))
    def question(self, obj, ar):
        return E.p(unicode(obj.question))

    @dd.displayfield(_("My answer"))
    def answer_buttons(self, obj, ar):
        l = []
        pv = dict(question=obj.question)
        ia = obj.response.toggle_choice
        for c in obj.question.get_choiceset().choices.all():
            pv.update(choice=c)
            text = unicode(c)
            try:
                AnswerChoice.objects.get(**pv)
                text = [E.b('[', text, ']')]
            except AnswerChoice.DoesNotExist:
                pass
            request_kwargs = dict(action_param_values=pv)
            e = ar.instance_action_button(
                ia, text, request_kwargs=request_kwargs,
                style="text-decoration:none")
            l.append(e)
        return E.p(*join_elems(l))


class PollResult(Questions):
    master_key = 'poll'
    column_names = "question choiceset answers a1"

    @classmethod
    def get_data_rows(self, ar):
        poll = ar.master_instance
        if poll is None:
            return
        for obj in super(PollResult, self).get_request_queryset(ar):
            yield obj

    @dd.virtualfield(dd.ForeignKey('polls.Question'))
    def question(self, obj, ar):
        return obj

    @dd.requestfield(_("#Answers"))
    def answers(self, obj, ar):
        #~ return ar.spawn(Answer.objects.filter(question=obj))
        return AnswerChoices.request(known_values=dict(question=obj))

    @dd.requestfield(_("A1"))
    def a1(self, obj, ar):
        c = iter(obj.get_choiceset().choices.all()).next()
        #~ return Answer.objects.filter(question=obj,choice=c)
        return AnswerChoices.request(
            known_values=dict(question=obj, choice=c))

   #~
#~ @dd.receiver(dd.database_ready)
#~ def on_database_ready(sender,**kw):
    #~ """
    #~ Builds columns dynamically from the :class:`PersonGroup` database table.
    #~
    #~ This must also be called before each test case.
    #~ """
    #~ self = PollResult
    #~ self.column_names = 'seqno text'
    #~ for obj in Questions.objects.filter(ref_name__isnull=False).order_by('ref_name'):
        #~ def w(pg):
            # ~ # we must evaluate `today` for each request, not only once when `database_ready`
            #~ today = datetime.date.today()
            #~ def func(self,obj,ar):
                #~ return Clients.request(
                    #~ param_values=dict(group=pg,
                        #~ coached_by=obj,start_date=today,end_date=today))
            #~ return func
        #~ vf = dd.RequestField(w(pg),verbose_name=pg.name)
        #~ self.add_virtual_field('G'+pg.ref_name,vf)
        #~ self.column_names += ' ' + vf.name
        #~
    #~ self.column_names += ' primary_clients active_clients row_total'
    # ~ self.clear_handle() # avoid side effects when running multiple test cases
    #~ settings.SITE.resolve_virtual_fields()


def setup_main_menu(site, ui, profile, m):
    m = m.add_menu("polls", config.verbose_name)
    m.add_action('polls.MyPolls')
    m.add_action('polls.MyResponses')


def setup_config_menu(site, ui, profile, m):
    m = m.add_menu("polls", config.verbose_name)
    m.add_action('polls.ChoiceSets')


def setup_explorer_menu(site, ui, profile, m):
    m = m.add_menu("polls", config.verbose_name)
    m.add_action('polls.Polls')
    m.add_action('polls.Questions')
    m.add_action('polls.Choices')
    m.add_action('polls.Responses')
    m.add_action('polls.AnswerChoices')
    m.add_action('polls.AnswerRemarks')
    #~ m.add_action('polls.Answers')


dd.add_user_group('polls', config.verbose_name)
