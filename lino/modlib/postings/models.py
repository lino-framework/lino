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
Defines models for :mod:`lino.modlib.outbox`.
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


from lino import mixins
#~ from lino.mixins import mails
from lino import tools
from lino import dd
#~ from lino.utils.babel import default_language
#~ from lino import reports
#~ from lino import layouts
#~ from lino.utils import perms
#~ from lino.utils import printable
from lino.utils import babel
#~ from lino.utils import call_optional_super
from django.conf import settings


from lino.utils.choicelists import ChoiceList



class PostingState(ChoiceList):
    """
    List of possible values for the `state` field of a 
    :class:`Posting`.
    """
    label = _("Posting State")
add = PostingState.add_item
add('10',_("Open"),'open') # owner still working on it
add('20',_("Ready to print"),'ready') # secretary can send it out
add('30',_("Printed"),'printed')
add('40',_("Sent"),'sent')
add('50',_("Returned"),'returned')
    

class Posting(mixins.AutoUser,mixins.Controllable):
    class Meta:
        verbose_name = _("Posting")
        verbose_name_plural = _("Postings")
    partner = models.ForeignKey('contacts.Partner',
        verbose_name=_("Recipient"),
        blank=True,null=True)
    state = PostingState.field()
    #~ sender = models.ForeignKey(settings.LINO.user_model)
    date = models.DateField()
    
    def save(self,*args,**kw):
        if not isinstance(self.owner,Postable):
            raise Exception("Controller of popsting must be a Postable.")
        super(Posting,self).save(*args,**kw)

    @dd.action(_("Print"))
    def print_action(self,ar):
        return self.owner.print_from_posting(self,ar)
    

class Postings(dd.Table):
    workflow_state_field = 'state'
    required=dict(user_level='manager')
    model = Posting
    column_names = 'date user owner partner *'
    #~ @dd.action()
    
class MyPostings(Postings,mixins.ByUser):
    required_user_level = None
    master_key = 'owner'
    column_names = 'date partner state workflow_buttons *'
  
class PostingsByController(Postings):
    required_user_level = None
    master_key = 'owner'
    column_names = 'date partner state workflow_buttons *'
  
class PostingsByPartner(Postings):
    required_user_level = None
    master_key = 'partner'
    column_names = 'date owner *'
    
    
class CreatePostings(dd.RowAction):
    """
    Creates a new Posting for each recipient.
    """
  
    url_action_name = 'post'
    #~ label = _('Create email')
    label = _('Post')
    callable_from = None
    
    def run(self,elem,ar,**kw):
        recs = tuple(elem.get_postable_recipients())
        ar.confirm(
          _("Going to create %(num)d postings for %(elem)s") 
          % dict(num=len(recs),elem=elem))
        for p in recs:
            p = Posting(owner=elem,partner=p,date=datetime.date.today())
            p.full_clean()
            p.save()
        #~ js = rr.renderer.instance_handler(m)
        #~ url = rr.renderer.js2url(js)
        #~ kw.update(open_url=rr.renderer.get_detail_url(m))
        #~ kw.update(open_url=url)
        kw.update(refresh=True)
        return ar.success_response(**kw)
        
    
    
class Postable(dd.Model):
    """
    Mixin for models that provide a "Post" button.
    """

    class Meta:
        abstract = True
        
    create_postings = CreatePostings()
    
    def print_from_posting(self,posting,ar):
        return ar.error_response("Not implemented")
        
    def get_postable_recipients(self):
        """return or yield a list of Partners"""
        return []
        

  

MODULE_LABEL = _("Outbox")
  
def setup_main_menu(site,ui,user,m): pass

def setup_my_menu(site,ui,user,m): 
    m  = m.add_menu("outbox",MODULE_LABEL)
    #~ m.add_action(MyInbox)
    m.add_action(MyPostings)
    #~ m.add_action(MySent)
  
def setup_config_menu(site,ui,user,m):
    pass
    #~ if user.level >= UserLevels.manager:
    #~ m  = m.add_menu("outbox",MODULE_LABEL)
    #~ m.add_action(MailTypes)
  
def setup_explorer_menu(site,ui,user,m):
    #~ if user.level >= UserLevels.manager:
    m  = m.add_menu("outbox",MODULE_LABEL)
    m.add_action(Postings)
  