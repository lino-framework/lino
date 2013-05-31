# -*- coding: utf-8 -*-
## Copyright 2008-2013 Luc Saffre
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

See :ref:`lino.tutorial.human`.
    
"""

import logging
logger = logging.getLogger(__name__)

import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext
from django.conf import settings

from lino.utils import join_words
from lino.core.choicelists import Genders

from lino.core import fields
from lino.core import model

#~ from lino import dd

#~ SHOW_SALUTATION = True
#~ UPPERCASE_LAST_NAME = True

#~ def uppercase_last_name(b):
    #~ global UPPERCASE_LAST_NAME
    #~ UPPERCASE_LAST_NAME = b

#~ def show_salutation(b):
    #~ global SHOW_SALUTATION
    #~ SHOW_SALUTATION = b


def get_salutation(gender,nominative=False):
    """
    Returns "Mr" or "Mrs" or a translation thereof, 
    depending on the gender and the current language.
    
    Note that the English abbreviations 
    `Mr <http://en.wikipedia.org/wiki/Mr.>`_ and 
    `Mrs <http://en.wikipedia.org/wiki/Mrs.>`_
    are written either with (AE) or without (BE) a dot. 
    
    The optional keyword argument `nominative` used only when babel language
    is "de": specifying ``nominative=True`` will return "Herr" instead of default 
    "Herrn" for male persons.
    
    """
    if not gender: return ''
    if gender == Genders.female: return _("Mrs")
    if nominative:
        return pgettext("nominative salutation","Mr") 
    return pgettext("indirect salutation","Mr") 
    





        

class Human(model.Model):
    """
    Base class for all models that represent a human.
    It defines three fields `first_name`, `last_name` and `gender`.
    
    """
    class Meta:
        abstract = True
        
    first_name = models.CharField(max_length=200,
      blank=True,
      verbose_name=_('First name'))
    "Space-separated list of all first names."
    
    last_name = models.CharField(max_length=200,
      blank=True,
      verbose_name=_('Last name'))
    """Last name (family name)."""
    
    gender = Genders.field(blank=True)
    
    def mf(self,m,f,u=None):
        """
        Taking three parameters `m`, `f` and `u` of any type, 
        returns one of them depending on whether this Person 
        is male, female or of unknown gender.
        
        See :mod:`lino.test_apps.gender` for some examples.
        
        """
        if self.gender is Genders.male: return m
        if self.gender is Genders.female: return f
        return u or m
        
    def __unicode__(self):
        return self.get_full_name(nominative=True)
      
    def get_salutation(self,**salutation_options):
        return get_salutation(
            #~ translation.get_language(),
            self.gender,**salutation_options)
    
    def get_full_name(self,salutation=True,upper=None,**salutation_options):
        """Returns a one-line string composed of salutation, first_name and last_name.
        
The optional keyword argument `salutation` can be set to `False` 
to suppress salutations. 
See :func:`lino_welfare.modlib.pcsw.tests.pcsw_tests.test04` 
and
:func:`lino.modlib.contacts.tests.test01` 
for some examples.

Optional `salutation_options` see :func:`get_salutation`.
        """
        #~ print '20120729 PersonMixin.get_full_name`'
        #~ return '%s %s' % (self.first_name, self.last_name.upper())
        words = []
        #~ if salutation is None:
            #~ salutation = SHOW_SALUTATION
        if salutation:
            words.append(self.get_salutation(**salutation_options))
        words.append(self.first_name)
        if upper is None:
            upper = settings.SITE.uppercase_last_name
        if upper:
            words.append(self.last_name.upper())
        else:
            words.append(self.last_name)
        #~ words += [self.first_name, self.last_name.upper()]
        return join_words(*words)
    full_name = property(get_full_name)
    
        
        
class Born(model.Model):
    """
    Abstract base class that adds a `birth_date` 
    field and a virtual field "Age".
    """
    class Meta:
        abstract = True
        
    birth_date = fields.IncompleteDateField(
        blank=True,verbose_name=_("Birth date"))
        
    
    def get_age_years(self,today=None):
        if self.birth_date and self.birth_date.year:
            if today is None:
                today = datetime.date.today()
            try:
                return today - self.birth_date.as_date()
            except ValueError:
                pass
      
    @fields.displayfield(_("Age"))
    def age(self,request,today=None):
        a = self.get_age_years(today)
        if a is None:
            return unicode(_('unknown'))
        s = _("%d years") % (a.days / 365)
        if self.birth_date and self.birth_date.is_complete():
            return s
        return u"±" + s


