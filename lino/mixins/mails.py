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
This module deserves more documentation.

"""
import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _


from lino import dd
from lino.utils.choicelists import ChoiceList
#~ from lino import mixins
from lino.mixins.printable import TypedPrintable

class RecipientType(ChoiceList):
    """A list of possible values for the `type` field of a 
    :class:`outbox.Recipient` or
    :class:`inbox.Recipient`.
    """
    label = _("Recipient Type")
    
add = RecipientType.add_item
#~ add('cc','cc',en=u"cc",de=u"Kopie an",   fr=u"cc")
#~ add('bcc','bcc',en=u"bcc",de=u"Versteckte Kopie an",   fr=u"bcc")
#~ add('to','to',en=u"to",de=u"an",   fr=u"à")
add('cc',_("cc"),alias='cc')
add('bcc',_("bcc"),alias='bcc')
add('to',_("to"),alias='to')

class Recipient(models.Model):

    allow_cascaded_delete = True
    
    class Meta:
        abstract = True
        verbose_name = _("Recipient")
        verbose_name_plural = _("Recipients")
    partner = models.ForeignKey('contacts.Partner',
        #~ verbose_name=_("Recipient"),
        blank=True,null=True)
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
        
    def full_clean(self):
        if self.partner:
            if not self.address:
                self.address = self.partner.email
            if not self.name:
                self.name = self.partner.get_full_name(salutation=False)
        super(Recipient,self).full_clean()
        

class Mail(TypedPrintable):
#~ class Mail(mixins.AutoUser):
    """
    Deserves more documentation.
    """
    
    class Meta:
        abstract = True
        verbose_name = _("Mail Message")
        verbose_name_plural = _("Mail Messages")
        
    #~ outgoing = models.BooleanField(verbose_name=_('Outgoing'))
    
    #~ sender = models.ForeignKey('contacts.Partner',
        #~ verbose_name=_("Sender"),
        #~ related_name='mails_by_sender',
        #~ blank=True,null=True)
    subject = models.CharField(_("Subject"),
        max_length=200,blank=True,
        #null=True
        )
    body = dd.RichTextField(_("Body"),blank=True,format='html')
    
    def get_print_language(self,bm):
        if self.sender is not None:
            return self.sender.language
        return super(Mail,self).get_print_language(bm)
        
    
    def __unicode__(self):
        return u'%s #%s ("%s")' % (self._meta.verbose_name,self.pk,self.subject)
        
    #~ def add_attached_file(self,fn):
        #~ """Doesn't work. 
        #~ """
        #~ kv = dict(type=settings.LINO.config.residence_permit_upload_type)
        #~ r = uploads.UploadsByOwner.request(master_instance=self)
        #~ r.create_instance(**kv)
      
    #~ @classmethod
    #~ def setup_report(cls,rpt):
        #~ mixins.TypedPrintable.setup_report(rpt)
        #~ rpt.add_action(SendMailAction())
        
