# -*- coding: utf-8 -*-
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

import logging
logger = logging.getLogger(__name__)

from lino.utils import i2d
from lino.core.dbutils import resolve_model
#Companies = resolve_model('contacts.Companies')
from djangosite.utils.djangotest import TestCase

#~ Person = resolve_model('contacts.Person')
#~ Property = resolve_model('properties.Property')
#~ PersonProperty = resolve_model('properties.PersonProperty')


class QuickTest(TestCase):
            
  
    def test01(self):
        """
        """
        from lino.modlib.cal.utils import DurationUnits
        
        start_date = i2d(20111026)
        self.assertEqual(DurationUnits.months.add_duration(start_date,2),i2d(20111226))
        self.assertEqual(DurationUnits.months.add_duration(start_date,-2),i2d(20110826))
        
        start_date = i2d(20110131)
        self.assertEqual(DurationUnits.months.add_duration(start_date,1),i2d(20110228))
        self.assertEqual(DurationUnits.months.add_duration(start_date,-1),i2d(20101231))
        self.assertEqual(DurationUnits.months.add_duration(start_date,-2),i2d(20101130))
        
        
        
        
        
