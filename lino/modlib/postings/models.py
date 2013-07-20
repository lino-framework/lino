# -*- coding: UTF-8 -*-
## Copyright 2012 Luc Saffre
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
Defines models for :mod:`lino.modlib.postings`.
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
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import IntegrityError
from django.utils.encoding import force_unicode
from django.core.exceptions import ValidationError

from django.conf import settings

from lino import mixins
#~ from lino.mixins import mails
from lino import dd
from lino.core import actions



class PostingStates(dd.Workflow):
    """
    List of possible values for the `state` field of a 
    :class:`Posting`.
    """
    #~ label = _("State")
    
add = PostingStates.add_item
add('10',_("Open"),'open') # owner still working on it
add('20',_("Ready to print"),'ready') # secretary can send it out
add('30',_("Printed"),'printed')
add('40',_("Sent"),'sent')
add('50',_("Returned"),'returned')
    

class Posting(mixins.AutoUser,mixins.ProjectRelated,mixins.Controllable):
    """
    A Posting is the fact that a letter or other item 
    has been sent using snail mail.
    """
    workflow_state_field = 'state'
    class Meta:
        verbose_name = _("Posting")
        verbose_name_plural = _("Postings")
        
    partner = models.ForeignKey('contacts.Partner',
        verbose_name=_("Recipient"),
        blank=True,null=True)
    state = PostingStates.field()
    #~ sender = models.ForeignKey(settings.SITE.user_model)
    date = models.DateField()
    
    def unused_save(self,*args,**kw):
        # see blog/2012/0929
        if not isinstance(self.owner,Postable):
            # raise Exception("Controller of a Posting must be a Postable.")
            raise ValidationError("Controller %s (%r,%r) is not a Postable" % (
                dd.obj2str(self.owner),self.owner_type,self.owner_id))
            #~ raise ValidationError("Controller %s is not a Postable" % dd.obj2str(self.owner))
        super(Posting,self).save(*args,**kw)

    @dd.action(_("Print"),icon_name='x-tbar-print')
    def print_action(self,ar,**kw):
        kw.update(refresh=True)
        r = self.owner.print_from_posting(self,ar,**kw)
        if self.state in (PostingStates.open,PostingStates.ready):
            self.state = PostingStates.printed
        self.save()
        return r
    

class Postings(dd.Table):
    required = dd.Required(user_level='manager',user_groups='office')
    model = Posting
    column_names = 'date user owner partner *'
    order_by = ['date']
    
    #~ @dd.action(_("Print"),icon_name='x-tbar-print')
    #~ def print_action(cls,ar,self,**kw):
        #~ kw.update(refresh=True)
        #~ r = self.owner.print_from_posting(self,ar,**kw)
        #~ if self.state in (PostingStates.open,PostingStates.ready):
            #~ self.state = PostingStates.printed
        #~ self.save()
        #~ return r
    
    
class MyPostings(Postings,mixins.ByUser):
    required = dd.Required(user_groups='office')
    #~ required = dict()
    #~ master_key = 'owner'
    column_names = 'date partner state workflow_buttons *'
  
class PostingsByState(Postings):
    required = dd.Required(user_groups='office',user_level='secretary')
    column_names = 'date user partner workflow_buttons *'
    
class PostingsReady(PostingsByState):
    label = _("Postings ready to print")
    known_values = dict(state=PostingStates.ready)
    
class PostingsPrinted(PostingsByState):
    label = _("Postings printed")
    known_values = dict(state=PostingStates.printed)
    
class PostingsSent(PostingsByState):
    label = _("Postings sent")
    known_values = dict(state=PostingStates.sent)
    
class PostingsByController(Postings):
    required = dd.Required(user_groups='office')
    master_key = 'owner'
    column_names = 'date partner state workflow_buttons *'
  
class PostingsByPartner(Postings):
    required = dd.Required(user_groups='office')
    master_key = 'partner'
    column_names = 'date owner state workflow_buttons *'
    
class PostingsByProject(Postings):
    required = dd.Required(user_groups='office')
    master_key = 'project'
    column_names = 'date partner state workflow_buttons *'
    
    
class CreatePostings(dd.RowAction):
    """
    Creates a series of new Postings from this Postable. 
    The Postable gives the list of recipients, and there will 
    be one Posting for each recipient.
    
    Author of each Posting will be the user who issued the action request,
    even if that user is acting as someone else.
    You cannot create a Posting in someone else's name.
    
    """
  
    url_action_name = 'post'
    #~ label = _('Create email')
    label = _('Create posting')
    help_text = _('Create classical mail postings from this')
    icon_name = 'x-tbar-create-postings'
    
    callable_from = (actions.GridEdit, 
        actions.ShowDetailAction,
        actions.ShowEmptyTable) # but not from InsertRow
    
    
    def run_from_ui(self,elem,ar,**kw):
        recs = tuple(elem.get_postable_recipients())
        ar.confirm(
          _("Going to create %(num)d postings for %(elem)s") 
          % dict(num=len(recs),elem=elem))
        for p in recs:
            p = Posting(
                  user=ar.user,owner=elem,partner=p,
                  date=datetime.date.today(),
                  state=PostingStates.ready)
            p.full_clean()
            p.save()
        kw.update(refresh=True)
        return ar.success(**kw)
        
    
    
class Postable(dd.Model):
    """
    Mixin for models that provide a "Post" button.
    """

    class Meta:
        abstract = True
        
    create_postings = CreatePostings()
    
    def print_from_posting(self,posting,ar,**kw):
        return ar.error("Not implemented")
        

  

#~ MODULE_LABEL = _("Outbox")
MODULE_LABEL = _("Postings")

system = dd.resolve_app('system')

def setup_main_menu(site,ui,profile,m):
    m  = m.add_menu("office",system.OFFICE_MODULE_LABEL)
    m  = m.add_menu("postings",MODULE_LABEL)
    m.add_action(MyPostings)
    m.add_action(PostingsReady)
    m.add_action(PostingsPrinted)
    m.add_action(PostingsSent)


  
#~ def setup_main_menu(site,ui,profile,m): pass

#~ def setup_my_menu(site,ui,profile,m): 
    #~ m  = m.add_menu("postings",MODULE_LABEL)
    #~ m.add_action(MyInbox)
    #~ m.add_action(MySent)
  
def setup_config_menu(site,ui,profile,m):
    pass
    #~ if user.level >= UserLevels.manager:
    #~ m  = m.add_menu("outbox",MODULE_LABEL)
    #~ m.add_action(MailTypes)
  
def setup_explorer_menu(site,ui,profile,m):
    #~ if user.level >= UserLevels.manager:
    m  = m.add_menu("office",system.OFFICE_MODULE_LABEL)
    #~ m  = m.add_menu("postings",MODULE_LABEL)
    m.add_action(Postings)
  
def get_todo_tables(ar):
    yield (PostingsReady,_("%d postings ready to print"))
                
  
