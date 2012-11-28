# -*- coding: UTF-8 -*-
## Copyright 2012 Luc Saffre
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

from django.utils.translation import ugettext_lazy as _

from lino.utils.choicelists import Choice,ChoiceList


class FiscalMonth(Choice):
    pass
    
class FiscalMonths(ChoiceList):
    item_class = FiscalMonth
    verbose_name = _("Fiscal Month")
    
    
class FiscalYear(Choice):
    pass
    
    #~ def __init__(self,lst,value=None,text=None,name=None,monthly=True,**kw):
        #~ s = str(year)  
        #~ super(FiscalYear,self).__init__(lst,s[2:],s)
        #~ if monthly:
        
    
class FiscalYears(ChoiceList):
    item_class = FiscalYear
    verbose_name = _("Fiscal Year")
    verbose_name_plural = _("Fiscal Years")
    
    @classmethod
    def from_int(cls,year):
        return cls.get_by_value(str(year)[2:])

for y in range(2000,datetime.date.today().year+5):
    s = str(y)
    FiscalYears.add_item(s[2:],s)

 



def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()

