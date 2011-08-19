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

"""
Defines models for :mod:`lino.modlib.mails`.
"""

import logging
logger = logging.getLogger(__name__)

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

from lino.utils.html2text import html2text
from django.core.mail import EmailMultiAlternatives
from lino.utils.config import find_config_file
from Cheetah.Template import Template as CheetahTemplate

class CreateMailAction(reports.RowAction):
    "Deserves more documentation."
  
    name = 'send'
    label = _('Create email')
    callable_from = None
            
    def run(self,rr,elem,**kw):
        #~ if False: 
            #~ if elem.time_sent:
                #~ return rr.ui.error_response(
                    #~ message="%s has already been sent (%s)" % (elem,elem.time_sent))
          
        tplname = elem._meta.app_label + '/' + elem.__class__.__name__ + '/email.html'
        
        
        fn = find_config_file(tplname)
        logger.info("Using email template %s",fn)
        tpl = CheetahTemplate(file(fn).read())
        tpl.instance = elem
        html_content = unicode(tpl)
        
        from lino.modlib.mails.models import OutMail
        m = OutMail(user=rr.get_user(),subject=elem.get_subject(),body=html_content)
        m.full_clean()
        m.save()
        for t,n,a in elem.get_recipients():
            m.recipient_set.create(type=t,address=a,name=n)
        kw.update(open_url=rr.ui.get_detail_url(m))
        return rr.ui.success_response(**kw)
        
    
class Mailable(models.Model):
    """
    Mixin for models that provide a "Create Email" button.
    Deserves more documentation.
    """

    class Meta:
        abstract = True
        
    #~ time_sent = models.DateTimeField(null=True,editable=False)
    
    @classmethod
    def setup_report(cls,rpt):
        rpt.add_action(CreateMailAction())
        
    def get_print_language(self,pm):
        return babel.DEFAULT_LANGUAGE
        
    #~ def get_templates_group(self):
        #~ return model_group(self)
        
    def get_subject(self):
        """
        Return the content of the `subject` 
        field for the email to be created.
        """
        return unicode(self)
        
    def get_recipients(self):
        "return or yield a list of (type,name,address) tuples"
        raise NotImplementedError()
        




class SendMailAction(reports.RowAction):
    "Deserves more documentation."
  
    name = 'send'
    label = _('Send email')
    callable_from = None
            
    def run(self,rr,elem,**kw):
        text_content = html2text(elem.body)
        #~ subject = elem.subject
        #~ sender = "%s <%s>" % (rr.get_user().get_full_name(),rr.get_user().email)
        sender = "%s <%s>" % (elem.user.get_full_name(),elem.user.email)
        #~ recipients = list(elem.get_recipients_to())
        msg = EmailMultiAlternatives(subject=elem.subject, 
            from_email=sender,
            body=text_content, 
            to=[r.name_address() for r in elem.recipient_set.filter(type=RecipientType.to)])
        msg.attach_alternative(elem.body, "text/html")
        msg.send()
      
        elem.sent = datetime.datetime.now()
        elem.save()
        kw.update(refresh=True)
        msg = "%s has been sent." % elem
        kw.update(message=msg)
        for n in """EMAIL_HOST SERVER_EMAIL EMAIL_USE_TLS EMAIL_BACKEND""".split():
            msg += "\n" + n + " = " + unicode(getattr(settings,n))
        logger.info(msg)
        return rr.ui.success_response(**kw)
      



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
    
    def name_address(self):
        return '%s <%s>' % (self.name,self.address)      
        
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
        return u'%s #%s ("%s")' % (self._meta.verbose_name,self.pk,self.subject)
        
    def add_attached_file(self,fn):
        """Doesn't work. 
        """
        kv = dict(type=settings.LINO.config.residence_permit_upload_type)
        r = uploads.UploadsByOwner.request(master_instance=self)
        r.create_instance(**kv)
      
        
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
    
    @classmethod
    def setup_report(cls,rpt):
        rpt.add_action(SendMailAction())


if False:
    """Won't work because Uploadable is only for files under /media/uploads"""
    class Attachment(mixins.Uploadable):
        
        
        class Meta:
            verbose_name = _("Attachment")
            verbose_name_plural = _("Attachments")
            
        mail = models.ForeignKey('mails.OutMail')
    


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
  