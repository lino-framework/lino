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

Defines the :class:`FiscalYears` choicelist.

"""
import datetime

from django.utils.translation import ugettext_lazy as _

#~ from lino.utils.choicelists import Choice,ChoiceList

from lino import dd

from django.conf import settings

#~ class FiscalMonth(dd.Choice):
    #~ pass
    
#~ class FiscalMonths(dd.ChoiceList):
    #~ item_class = FiscalMonth
    #~ verbose_name = _("Fiscal Month")
    
    
class FiscalYear(dd.Choice):
    pass
    
    
class FiscalYears(dd.ChoiceList):
    """
    If the fiscal year of your company is the same as the calendar 
    year, then the default entries in this should do.
    Otherwise you can always override this in your 
    :meth:`lino.Lino.setup_choicelists`.
    """
    item_class = FiscalYear
    verbose_name = _("Fiscal Year")
    verbose_name_plural = _("Fiscal Years")
    #~ preferred_width = 4 # would be 2 otherwise 
    
    #~ @classmethod
    #~ def setup_field(cls,fld):
        #~ def d(): return cls.from_date(datetime.date.today())
        #~ fld.default = d
        #~ print 20121227, cls.preferred_width
        
    @classmethod
    def from_int(cls,year):
        return cls.get_by_value(str(year)[2:])
        
    @classmethod
    def from_date(cls,date):
        return cls.from_int(date.year)

for y in range(settings.SITE.start_year,datetime.date.today().year+5):
    s = str(y)
    FiscalYears.add_item(s[2:],s)

 

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()

