# -*- coding: UTF-8 -*-
## Copyright 2011-2013 Luc Saffre
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
The :xfile:`models.py` module for :ref:`cosi`.
"""

import os
import cgi
import datetime

from django.db import models
#~ from django.db.models import Q
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


#~ from lino import mixins
from lino import dd

#~ contacts = dd.resolve_app('contacts')
#~ sales = dd.resolve_app('sales')

#~ class Partner(contacts.Partner,sales.Customer):
    #~ class Meta(contacts.Partner.Meta):
        #~ app_label = 'contacts'
        
#~ class Person(contacts.Person,sales.Customer):
    #~ class Meta(contacts.Person.Meta):
        #~ app_label = 'contacts'

#~ class Company(contacts.Company,sales.Customer):
    #~ class Meta(contacts.Company.Meta):
        #~ app_label = 'contacts'

#~ def site_setup(site):
    #~ site.description = 
    
    
@dd.when_prepared('partners.Person','partners.Organisation')
def hide_region(model):
    model.hide_elements('region')

        
@dd.receiver(dd.pre_analyze)
def set_merge_actions(sender,**kw):
    #~ logger.info("%s.set_merge_actions()",__name__)
    partners = sender.modules[settings.SITE.partners_app_label]
    #~ print 20130202, app.keys()
    for m in (partners.Person,partners.Organisation):
        #~ print repr(m)
        m.define_action(merge_row=dd.MergeAction(m))
        #~ m.merge_row = dd.MergeAction(m)
        #~ m.hide_elements('region')
    
    #~ modules.contacts.PartnerDetail.address_box.remove_element('region')
    #~ modules.contacts.Partner.hide_elements('region')
