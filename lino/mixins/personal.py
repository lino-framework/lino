## Copyright 2010-2011 Luc Saffre
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

"""

import datetime

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils import translation 

from lino.modlib.contacts.utils import SEX_CHOICES, get_salutation
from lino.utils import join_words


def SexField(**kw):
    options = dict(max_length=1,blank=True,null=True,
        verbose_name=_("Sex"),choices=SEX_CHOICES) 
    options.update(kw)
    return models.CharField(**options)
        

class PersonMixin(models.Model):
    """
    Base class for models that represent a physical person. 
    """
    class Meta:
        abstract = True
        #~ app_label = 'contacts'
        #~ verbose_name = _("Person")
        #~ verbose_name_plural = _("Persons")

    first_name = models.CharField(max_length=200,blank=True,
      verbose_name=_('First name'))
    "Space-separated list of all first names."
    
    last_name = models.CharField(max_length=200,blank=True,
      verbose_name=_('Last name'))
    "Last name (family name)."
    
    title = models.CharField(max_length=200,blank=True,
      verbose_name=_('Title'))
    "Text to print as part of the first address line in front of first_name."
        
    sex = SexField()
        
    def get_salutation(self,**salutation_options):
        return get_salutation(
            translation.get_language(),
            self.sex,**salutation_options)
    
        
    def get_full_name(self,salutation=True,**salutation_options):
        """Returns a one-line string composed of salutation, first_name and last_name.
        
The optional keyword argument `salutation` can be set to `False` 
to suppress salutations. 
See :func:`lino.apps.dsbe.tests.dsbe_tests.test04` 
and
:func:`lino.modlib.contacts.tests.test01` 
for some examples.

Optional `salutation_options` see :func:`get_salutation`.
        """
        #~ return '%s %s' % (self.first_name, self.last_name.upper())
        words = []
        if salutation:
            words.append(self.get_salutation(**salutation_options))
        words += [self.first_name, self.last_name.upper()]
        return join_words(*words)
    full_name = property(get_full_name)
    #~ full_name.return_type = models.CharField(max_length=200,verbose_name=_('Full name'))
    
    def address_person_lines(self,*args,**kw):
        "Deserves more documentation."
        if self.title:
            yield self.title
        yield self.get_full_name(*args,**kw)
        #~ l = filter(lambda x:x,[self.first_name,self.last_name])
        #~ yield  " ".join(l)
        
    def full_clean(self,*args,**kw):
        l = filter(lambda x:x,[self.last_name,self.first_name])
        self.name = " ".join(l)
        super(PersonMixin,self).full_clean(*args,**kw)


