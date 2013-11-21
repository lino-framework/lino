# -*- coding: UTF-8 -*-
## Copyright 2012-2013 Luc Saffre
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

A special settings module to be used as DJANGO_SETTINGS_MODULE 
when Sphinx generates the Lino docs.

It contains *all* modlib modules, which makes no sense in practice 
and would raise errors if you try to initialize a database or 
validate the models, but it is enough to have autodocs do its job. 
And that's all we want.

"""

import os
import lino

from lino.projects.std.settings import *

from lino.modlib import vat

class Site(Site,vat.SiteMixin):

    verbose_name = "Lino Docs"
    
    project_model = 'contacts.Person'
    user_model = 'users.User'
    
    languages = 'en'
    
    def get_installed_apps(self):
        for a in super(Site,self).get_installed_apps():
            yield a

        yield 'lino.modlib.system'
        yield 'django.contrib.contenttypes'
        yield 'lino.modlib.users'
        yield 'lino.modlib.changes'
        yield 'lino.modlib.countries'
        yield 'lino.modlib.properties'
        yield 'lino.modlib.contacts'
        
        yield 'lino.modlib.uploads'
        yield 'lino.modlib.notes'
        yield 'lino.modlib.outbox'
        yield 'lino.modlib.cal'
        yield 'lino.modlib.postings'
        yield 'lino.modlib.households'
        
        yield 'lino.modlib.accounts'
        yield 'lino.modlib.ledger'
        yield 'lino.modlib.vat'
        yield 'lino.modlib.products'
        yield 'lino.modlib.auto.sales'
        yield 'lino.modlib.concepts'
        yield 'lino.modlib.courses'
        yield 'lino.modlib.pages'
        #~ yield 'lino.projects.cosi'
        #~ yield 'lino'

SITE = Site(globals())
#~ print 20130409, __file__, LOGGING

