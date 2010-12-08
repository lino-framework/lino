## Copyright 2010 Luc Saffre
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


from django.db import models
from django.utils.translation import ugettext_lazy as _

from lino import reports
from lino import fields
from lino.utils import join_words
from lino.utils.babel import add_babel_field, default_language, babelattr
    

class Addressable(models.Model):
    """
    
Anything that has contact information (postal address, email, phone,...).

.. attribute:: country

    A pointer to :class:`countries.Country`. The country where this contact is located.
  
.. attribute:: city

    A pointer to :class:`countries.City`. The city where this contact is located.
    The list of choices for this field is context-sensitive, it depends on the :attr:`country`.
  
.. method:: address

    The plain text postal address, laid out according to the local rules in 
    this Addressable's :country. 
    Virtual field. 

    
    """
  
    class Meta:
        abstract = True
  
    name = models.CharField(max_length=200,verbose_name=_('Name'))
    street = models.CharField(_("Street"),max_length=200,blank=True)
    street_no = models.CharField(_("No."),max_length=10,blank=True)
    street_box = models.CharField(_("Box"),max_length=10,blank=True)
    addr1 = models.CharField(max_length=200,blank=True)
    #addr2 = models.CharField(max_length=200,blank=True)
    
    country = models.ForeignKey('countries.Country',blank=True,null=True,
      verbose_name=_("Country"))
    "See :meth:`contacts.Contact.country`"
    
    city = models.ForeignKey('countries.City',blank=True,null=True,
        verbose_name=_('City'))
    "See :meth:`contacts.Contact.city`"
    
    #city = models.CharField(max_length=200,blank=True)
    zip_code = models.CharField(_("Zip code"),max_length=10,blank=True)
    region = models.CharField(_("Region"),max_length=200,blank=True)
    #~ language = models.ForeignKey('countries.Language',default=default_language)
    language = fields.LanguageField(default=default_language)
    
    email = models.EmailField(_('E-Mail'),blank=True,null=True)
    url = models.URLField(blank=True,verbose_name=_('URL'))
    phone = models.CharField(max_length=200,blank=True,verbose_name=_('Phone'))
    gsm = models.CharField(max_length=200,blank=True,verbose_name=_('GSM'))
    fax = models.CharField(max_length=200,blank=True,verbose_name=_('Fax'))
    #image = models.ImageField(blank=True,null=True,
    # upload_to=".")
    
    remarks = models.TextField(blank=True,null=True)
    
    def __unicode__(self):
        return self.name
        
    def recipient_lines(self):
        yield self.name
        
    def address(self,linesep="\n<br/>"):
        "Implements :meth:`contacts.Contact.address`"
        return linesep.join(self.address_lines()) # ', ')
    address.return_type = models.TextField(_("Address"))
    
        
    def address_lines(self,linesep="\n<br/>"):
        #~ lines = []
        #~ lines = [self.name]
        if self.addr1:
            yield self.addr1
        if self.street:
            yield join_words(self.street,self.street_no,self.street_box)
        #lines = [self.name,street,self.addr1,self.addr2]
        if self.region: # format used in Estonia
            if self.city:
                yield unicode(self.city)
            s = join_words(self.zip_code,self.region)
        else: 
            s = join_words(self.zip_code,self.city)
        if s:
            yield s 
        foreigner = True # False
        #~ if self.id == 1:
            #~ foreigner = False
        #~ else:
            #~ foreigner = (self.country != self.objects.get(pk=1).country)
        if foreigner and self.country: # (if self.country != sender's country)
            yield unicode(self.country)
        #~ logger.debug('%s : as_address() -> %r',self,lines)
        #~ return mark_safe(linesep.join(lines))
        
    @classmethod
    def city_choices(cls,country):
        #print "city_choices", repr(recipient)
        #recipient = self.objects.get(pk=pk)
        if country is not None:
        #if recipient and recipient.country:
            return country.city_set.order_by('name')
        return cls.city.field.rel.to.objects.order_by('name')
        #return countries.City.oiesByCountry().get_queryset(master_instance=recipient.country)
        #return dict(country__in=(recipient.country,))
        
    def on_create(self,request):
        pass
        #~ print "lino.modlib.contacts.Contacts.on_create()"
        #~ instance.language = 
        
class Addressables(reports.Report):
    column_names = "name * id" 
    def get_queryset(self):
        return self.model.objects.select_related('country','city')
  

