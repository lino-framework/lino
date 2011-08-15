# -*- coding: UTF-8 -*-
## Copyright 2011 Luc Saffre
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

import os
import sys
import cgi
import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import IntegrityError
from django.utils.encoding import force_unicode


from lino import fields, tools
#~ from lino.utils.babel import default_language
from lino import reports
#~ from lino import layouts
from lino.utils import perms
from lino.utils.restify import restify
#~ from lino.utils import printable
from lino.utils import babel
from lino import mixins
from django.conf import settings
#~ from lino import choices_method, simple_choices_method

from lino.modlib.mails.utils import RecipientType


class Recipient(models.Model):
#~ class Recipient(mixins.Owned):
  
    class Meta:
        verbose_name = _("Recipient")
        verbose_name_plural = _("Recipients")
    mail = models.ForeignKey('mails.Mail')
    type = RecipientType.field()
    address = models.EmailField(_("Address"))
    name = models.CharField(_("Name"),max_length=200)
    #~ address_type = models.ForeignKey(ContentType)
    #~ address_id = models.PositiveIntegerField()
    #~ address = generic.GenericForeignKey('address_type', 'address_id')
    
    def __unicode__(self):
        return "[%s]" % unicode(self.name or self.address)
        #~ return "[%s]" % unicode(self.address)

class Recipients(reports.Report):
    model = 'mails.Recipient'
    #~ column_names = 'mail  type *'
    #~ order_by = ["address"]

class RecipientsByMail(Recipients):
    fk_name = 'mail'
    column_names = 'type address name'
    #~ column_names = 'type owner_type owner_id'
    #~ column_names = 'type owner'

class Mail(models.Model):
    """
    Deserves more documentation.
    """
    #~ class Meta:
        #~ abstract = True
        #~ verbose_name = _("Mail")
        #~ verbose_name_plural = _("Mails")
        
    #~ outgoing = models.BooleanField(verbose_name=_('Outgoing'))
    
    subject = models.CharField(_("Subject"),max_length=200,blank=True,null=True)
    body = fields.RichTextField(_("Body"),blank=True,format='html')
    
    def get_recipients(self,rr):
        #~ recs = []
        recs = [ unicode(r) for r in 
            Recipient.objects.filter(mail=self,type=RecipientType.to)]
          
            #~ s = rr.ui.href_to(r.owner)
            #~ if r.type != RecipientType.to:
                #~ s += "(%s)" % r.type
            #~ recs.append(s)
        return ', '.join(recs)
    recipients = fields.VirtualField(fields.HtmlBox(_("Recipients")),get_recipients)
        
        
    #~ def recipients_to(self,rr):
        #~ kv = dict(type=RecipientType.to)
        #~ r = rr.spawn_request(RecipientsByMail(),
              #~ master_instance=self,
              #~ known_values=kv)
        #~ return rr.ui.quick_upload_buttons(r)
    #~ recipients_to.return_type = fields.DisplayField(_("to"))
    
    def __unicode__(self):
        return u'%s #%s' % (self._meta.verbose_name,self.pk)
        
class InMail(Mail):
    "Incoming Mail"
    
    class Meta:
        verbose_name = _("Incoming Mail")
        verbose_name_plural = _("Incoming Mails")
        
    sender_type = models.ForeignKey(ContentType,blank=True,null=True)
    sender_id = models.PositiveIntegerField(blank=True,null=True)
    sender = generic.GenericForeignKey('sender_type', 'sender_id')
    received = models.DateTimeField(auto_now_add=True,editable=False)
    
class OutMail(Mail,mixins.AutoUser):
    "Outgoing Mail"
    
    class Meta:
        verbose_name = _("Outgoing Mail")
        verbose_name_plural = _("Outgoing Mails")
        
    sent = models.DateTimeField(null=True,editable=False)
    

    


class Mails(reports.Report):
    model = 'mails.Mail'
    
class InMails(reports.Report):
    model = 'mails.InMail'
    column_names = "received sender subject * body"
    order_by = ["received"]

class OutMails(reports.Report):
    model = 'mails.OutMail'
    column_names = "sent user subject * body"
    order_by = ["sent"]
    

class MyOutMails(mixins.ByUser,OutMails):  pass
    #~ known_values = dict(outgoing=True)
    #~ label = _("My Outgoing Mails")

class MyInMails(InMails): 
    #~ known_values = dict(outgoing=False)
    label = _("My Incoming Mails")
    
    def setup_request(self,rr):
        rr.known_values.update(recipient__address=rr.get_user().email)
        #~ if rr.master_instance is None:
            #~ rr.master_instance = rr.get_user()
    

class MailsByPerson(object):
    master = 'contacts.Person'
    can_add = perms.never
    
    def get_master_kw(self,master_instance,**kw):
        #~ ct = ContentType.objects.get_for_model(master_instance.__class__)
        #~ skw[self.fk.ct_field] = ct
        #~ skw[self.fk.fk_field] = master_instance.pk
        #~ q1 = Recipient.objects.filter(owner_type=ct,owner_id=master_instance.pk)
        q1 = Recipient.objects.filter(address=master_instance.email).values('mail').query
        #~ q1 = Recipient.objects.filter(address=master_instance.email)
        kw['id__in'] = q1
        #~ kw['recipient_set__address__contains'] = master_instance
        return kw

  
class InMailsByPerson(MailsByPerson,InMails):
    column_names = 'received subject sender'
    order_by = ['received']

class OutMailsByPerson(MailsByPerson,OutMails): 
    column_names = 'sent subject recipients'
    order_by = ['sent']
    
  
def setup_main_menu(site,ui,user,m): pass

def setup_my_menu(site,ui,user,m): 
    m.add_action('mails.MyInMails')
    m.add_action('mails.MyOutMails')
  
def setup_config_menu(site,ui,user,m): pass
  
def setup_explorer_menu(site,ui,user,m):
    m  = m.add_menu("mails",_("~Mails"))
    m.add_action('mails.Mails')
  