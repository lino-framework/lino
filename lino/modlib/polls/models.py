# -*- coding: UTF-8 -*-
## Copyright 2013 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.
"""
The :xfile:`models` module for :mod:`lino.modlib.polls`.

A Poll is a collection of Questions
A Question is a question text and a ChoiceSet.
A ChoiceSet is a stored ordered set of possible Choices.
A Response is when a User answers to a Poll. 
A Response is a set of Answers, one Answer for each Question of the Poll.

An Answer is when a given User selects a given Choice for a given Question
"""

import logging
logger = logging.getLogger(__name__)

import os
import sys
import cgi
import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy 

#~ from django.contrib.contenttypes.models import ContentType
#~ from django.contrib.contenttypes import generic
from django.db import IntegrityError
from django.utils.encoding import force_unicode


#~ from lino import tools
from lino import dd
#~ from lino import reports
#~ from lino import layouts
#~ from lino.utils import perms
from lino.utils.restify import restify
from lino.utils import join_elems
#~ from lino.utils import printable
from lino import mixins
from django.conf import settings
from lino.utils.xmlgen.html import E

#~ from lino import choices_method, simple_choices_method
#~ from lino.modlib.contacts import models as contacts
#~ from lino.modlib.outbox import models as outbox
#~ from lino.modlib.postings import models as postings


from lino.modlib.polls import App

outbox = dd.resolve_app('outbox')
postings = dd.resolve_app('postings')
contacts = dd.resolve_app('contacts')


#~ def NullBooleanField(*args,**kw):
    #~ kw.setdefault('default',False)
    #~ return models.BooleanField(*args,**kw)
#~ # not yet implemented:
NullBooleanField = models.NullBooleanField


class PollStates(dd.Workflow):
    """
    State of a Calendar Task. Used as Workflow selector.
    """
    verbose_name_plural = _("Poll States")
    required = dd.required(user_level='admin')
    
    
add = PollStates.add_item
add('10', _("Draft"),'draft')
add('20', _("Published"),'published')
add('30', _("Closed"),'closed')



class ResponseStates(dd.Workflow):
    """
    Possible states of a Response.
    """
    verbose_name_plural = _("Response States")
    required = dd.required(user_level='admin')
    
    
add = ResponseStates.add_item
add('10', _("Draft"),'draft',editable=True)
add('20', _("Registered"),'registered',editable=False)


ResponseStates.registered.add_transition(_("Register"),states='draft')
ResponseStates.draft.add_transition(_("Deregister"),states="registered")


#~ class QuestionTypes(dd.ChoiceList):
    #~ verbose_name_plural = _("Question Types")
    #~ required = dd.required(user_level='admin')
    #~ 
#~ add = QuestionTypes.add_item
#~ add('10', _("Draft"),'draft',editable=True)
    


class ChoiceSet(dd.BabelNamed):
    class Meta:
        verbose_name = _("Choice Set")
        verbose_name_plural = _("Choice Sets")
        
class ChoiceSets(dd.Table):
    model = ChoiceSet
    detail_layout = """
    name
    ChoicesBySet
    """
    
class Choice(dd.BabelNamed,dd.Sequenced):
    class Meta:
        verbose_name = _("Choice")
        verbose_name_plural = _("Choices")
        
    choiceset = models.ForeignKey('polls.ChoiceSet',related_name='choices')
    
    def get_siblings(self):
        return self.choiceset.choices.order_by('seqno')
    
class Choices(dd.Table):
    model = 'polls.Choice'
        
class ChoicesBySet(Choices):
    master_key = 'choiceset'

class Poll(dd.UserAuthored,dd.CreatedModified):
    
    class Meta:
        abstract = settings.SITE.is_abstract_model('polls.Poll')
        verbose_name = _("Poll")
        verbose_name_plural = _("Polls")
        ordering = ['created']
        
    title = models.CharField(_("Title"),max_length=200)
    
    details = models.TextField(_("Details"),blank=True)
    
    default_choiceset = models.ForeignKey('polls.ChoiceSet',
        null=True,blank=True,
        related_name='polls',
        verbose_name=_("Default Choiceset"))
    
    default_multiple_choices = NullBooleanField(
        _("Allow multiple choices"))
        #~ null=True,blank=True)
        
    questions_to_add = models.TextField(_("Questions to add"),
        help_text=_("Paste text for questions to add. Every non-empty line will create one question."),
        blank=True)
    
    state = PollStates.field(default=PollStates.draft)
    
    def __unicode__(self):
        return self.title
    
    def after_ui_save(self,ar):
        if self.questions_to_add:
            #~ print "20131106 self.questions_to_add", self.questions_to_add
            #~ qkw = dict(choiceset=self.default_choiceset)
            qkw = dict()
            for ln in self.questions_to_add.splitlines():
                ln = ln.strip()
                if ln:
                    q = Question(poll=self,text=ln,**qkw)
                    q.full_clean()
                    q.save()
                    qkw.setdefault('seqno',q.seqno+1)
            self.questions_to_add = ''
            self.save() # save again
                    
        super(Poll,self).after_ui_save(ar)
        
    @dd.virtualfield(dd.HtmlBox(_("Result")))
    def result(self,ar):
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
    """,label=_("General"))
    
    results = dd.Panel("""
    polls.ResponsesByPoll
    # result
    PollResult
    """,label=_("Results"))
    
class Polls(dd.Table):
    model = 'polls.Poll'
    column_names = 'created title user state *'
    detail_layout = PollDetail()
    insert_layout = dd.FormLayout("""
    title
    default_choiceset default_multiple_choices
    questions_to_add
    """,window_size=(60,15))
    
class MyPolls(dd.ByUser,Polls):
    column_names = 'created title state *'
    

class Question(dd.Sequenced):
    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")
        
    poll = models.ForeignKey('polls.Poll',related_name='questions')
    text = models.TextField(verbose_name=_("Text"))
    choiceset = models.ForeignKey('polls.ChoiceSet',blank=True,null=True)
    multiple_choices = NullBooleanField(_("Allow multiple choices"))
    
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
        
    def get_multiple_choices(self):
        if self.multiple_choices is None:
            return self.poll.default_multiple_choices
        return self.multiple_choices
        
    #~ def full_clean(self,*args,**kw):
        #~ if self.choiceset_id is None:
            #~ self.choiceset = self.poll.default_choiceset
        #~ super(Question,self).full_clean()
    
class Questions(dd.Table):
    model = 'polls.Question'
    
    
class QuestionsByPoll(Questions):
    master_key = 'poll'
    column_names = 'text choiceset multiple_choices'
    auto_fit_column_widths = True
    
class Response(dd.UserAuthored,dd.Registrable,dd.CreatedModified):
    class Meta:
        verbose_name = _("Response")
        verbose_name_plural = _("Responses")
        ordering = ['created']
        
    poll = models.ForeignKey('polls.Poll',related_name='responses')
    state = ResponseStates.field(default=ResponseStates.draft)
    remark = models.TextField(verbose_name=_("My general remark"),blank=True)
    
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
            user=self.user,poll=self.poll)
        
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
    def get_detail_title(self,ar,obj):
        txt = _("response to %(poll)s") % dict(poll=obj.poll)
        if obj.user == ar.get_user():
            return  _("My %s") % txt
        return _("%(user)s's %(what)s") % dict(user=obj.user,what=txt)
        
        
class MyResponses(dd.ByUser,Responses):
    column_names = 'created poll state remark *'
        
class ResponsesByPoll(Responses):
    master_key = 'poll'
    column_names = 'created user state remark *'
    
    
class AnswerChoice(dd.Model):
    class Meta:
        verbose_name = _("Answer Choice")
        verbose_name_plural = _("Answer Choices")
        ordering = ['question__seqno']
        
    response = models.ForeignKey('polls.Response')
    question = models.ForeignKey('polls.Question')
    choice = models.ForeignKey('polls.Choice',
        related_name='answers',verbose_name=_("My answer"),
        blank=True,null=True)
        
    @dd.chooser()
    def choice_choices(cls,question):
        return question.get_choiceset().choices.all()
        
    
class AnswerRemark(dd.Model):
    class Meta:
        verbose_name = _("Answer Remark")
        verbose_name_plural = _("Answer Remarks")
        ordering = ['question__seqno']
        
    response = models.ForeignKey('polls.Response')
    question = models.ForeignKey('polls.Question')
    remark = models.TextField(_("My remark"),blank=True)
        
        
    

FORWARD_TO_QUESTION = tuple("full_clean after_ui_save disable_delete".split())

"""
volatile object to represent "the one and only" answer to a given question 
in a given response
"""
class Answer(object):
    def __init__(self,response,question):
        self.response = response
        self.question = question
        self.pk = self.id = question.pk
        try:
            self.remark = AnswerRemark.objects.get(question=question,response=response)
        except AnswerRemark.DoesNotExist:
            self.remark = AnswerRemark(question=question,response=response)
            
        self.choices = AnswerChoice.objects.filter(question=question,response=response)
        for k in FORWARD_TO_QUESTION:
            setattr(self,k,getattr(question,k))
        
        
class AnswerRemarkField(dd.VirtualField):
    """
    An editable virtual field.
    """
    editable = True
    def __init__(self):
        rt = models.TextField(_("My remark"),blank=True)
        dd.VirtualField.__init__(self,rt,None)
    
    def set_value_in_object(self,ar,obj,value):
        #~ e = self.get_entry_from_answer(obj)
        obj.remark.remark = value
        obj.remark.save()
        
    def value_from_object(self,obj,ar):
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
    def get_row_by_pk(self,ar,pk):
        response = ar.master_instance
        #~ if response is None: return
        q = Question.objects.get(pk=pk)
        return Answer(response,q)
        
    @classmethod
    def get_row_permission(cls,obj,ar,state,ba):
        return True
        
        
    @classmethod
    def disable_delete(self,obj,ar):
        return "Not deletable"
        
    @classmethod
    def get_data_rows(self,ar):
        response = ar.master_instance
        if response is None: return 
        for q in Question.objects.filter(poll=response.poll):
            yield Answer(response,q)
    
    @dd.displayfield(_("Question"))
    def question(self,obj,ar):
        return E.p(unicode(obj.question))
        
    @dd.displayfield(_("My answer"))
    def answer_buttons(self,obj,ar):
        l = []
        if obj.question.get_multiple_choices():
            l.append("MC not yet implemented")
        else:
            kw = dict(title=_("Select this value"))
            for c in obj.question.get_choiceset().choices.all():
                l.append(unicode(c))
                #~ l.append(ar.put_button(obj.question,unicode(c),dict(choice=c),**kw))
                #~ l.append(self.select_choice.as_button_elem(ar.request,unicode(c)))
        return E.p(*join_elems(l))
    
        

    
class PollResult(Questions):
    master_key = 'poll'
    column_names = "question choiceset answers a1"
    
    @classmethod
    def get_data_rows(self,ar):
        poll = ar.master_instance
        if poll is None: return 
        for obj in super(PollResult,self).get_request_queryset(ar):
            yield obj
            
    @dd.virtualfield(dd.ForeignKey('polls.Question'))
    def question(self,obj,ar):
        return obj
        
    @dd.requestfield(_("#Answers"))
    def answers(self,obj,ar):
        #~ return ar.spawn(Answer.objects.filter(question=obj))
        return Answers.request(known_values=dict(question=obj))
        
    @dd.requestfield(_("A1"))
    def a1(self,obj,ar):
        c = iter(obj.get_choiceset().choices.all()).next()
        #~ return Answer.objects.filter(question=obj,choice=c)
        return Answers.request(known_values=dict(question=obj,choice=c))
        
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
            #~ # we must evaluate `today` for each request, not only once when `database_ready`
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
    #~ self.clear_handle() # avoid side effects when running multiple test cases
    #~ settings.SITE.resolve_virtual_fields()

    


def setup_main_menu(site,ui,profile,m):
    m  = m.add_menu("polls",App.verbose_name)
    m.add_action('polls.MyPolls')
    m.add_action('polls.MyResponses')
  
def setup_config_menu(site,ui,profile,m): 
    m  = m.add_menu("polls",App.verbose_name)
    m.add_action('polls.ChoiceSets')
  
def setup_explorer_menu(site,ui,profile,m):
    m  = m.add_menu("polls",App.verbose_name)
    m.add_action('polls.Polls')
    m.add_action('polls.Questions')
    m.add_action('polls.Choices')
    m.add_action('polls.Responses')
    #~ m.add_action('polls.Answers')
  

dd.add_user_group('polls',App.verbose_name)
