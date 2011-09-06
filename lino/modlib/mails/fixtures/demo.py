# -*- coding: UTF-8 -*-
## Copyright 2008-2011 Luc Saffre
## This file is part of the Lino-DSBE project.
## Lino-DSBE is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino-DSBE is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino-DSBE; if not, see <http://www.gnu.org/licenses/>.


#~ from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db import models

from lino.utils.instantiator import Instantiator, i2d
from lino.tools import resolve_model
from lino.utils.babel import babel_values, babelitem
from lino.modlib.mails.utils import RecipientType


#~ from lino.modlib.properties import models as properties 

def objects():
  
    Person = resolve_model('contacts.Person')
    Company = resolve_model('contacts.Company')
    User = resolve_model(settings.LINO.user_model)
    
    root = User.objects.get(username='root')
    
    outmail = Instantiator('mails.OutMail').build
    inmail = Instantiator('mails.InMail').build
    recipient_to = Instantiator('mails.Recipient',type=RecipientType.to).build
    
    #~ for p in Person.objects.filter(email__isnull=True):
    for p in Person.objects.filter(email=''):
        try:
            p.first_name.encode('ascii')
            p.email = p.first_name.lower() + "@example.com"
            p.save()
        except UnicodeError:
            pass
            
    for person in Person.objects.exclude(email=''):
    #~ for person in Person.objects.filter(email__isnull=False):
        m = outmail(user=root,subject='Welcome %s!' % person.first_name)
        yield m
        yield recipient_to(mail=m,contact=person)
            #~ address=person.email,name=person.get_full_name(salutation=False))
    
