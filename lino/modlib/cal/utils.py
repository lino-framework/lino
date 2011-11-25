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

from django.utils.translation import ugettext_lazy as _

from lino.utils.choicelists import ChoiceList

from dateutil.tz import tzlocal

def aware(d):
    return datetime.datetime(d.year,d.month,d.day,tzinfo=tzlocal())

def dt2kw(dt,name,**d):
    """
    Store given timestamp `dt` in a field dict. `name` can be 'start' or 'end'. 
    """
    if dt:
        if isinstance(dt,datetime.datetime):
            d[name+'_date'] = dt.date()
            if dt.time():
                d[name+'_time'] = dt.time()
            else:
                d[name+'_time'] = None
        elif isinstance(dt,datetime.date):
            d[name+'_date'] = dt
            d[name+'_time'] = None
        else:
            raise Exception("Invalid datetime value %r" % dt)
    else:
        d[name+'_date'] = None
        d[name+'_time'] = None
    return d
  
def setkw(obj,**kw):
    for k,v in kw.items():
        setattr(obj,k,v)
                              



class DurationUnit(ChoiceList):
    """A list of possible values for the `duration_unit` field of an :class:`Event`.
    """
    label = _("Duration Unit")
    
    @classmethod
    def add_duration(cls,unit,dt,value):
        """
        Return a date or datetime obtained by adding `value` 
        times the specified unit.
        
        This is intended for use as a 
        `curried magic method` of a specified list item:
        
        >>> start_date = datetime.date(2011,10,26)
        >>> DurationUnit.months.add_duration(start_date,2)
        datetime.date(2011,12,26)
        
        See more usage examples in :func:`lino.modlib.cal.tests.cal_test.test01`.
        """
        if dt is None: 
            return None
        if unit.value == 's' : 
            return dt + datetime.timedelta(seconds=value)
        if unit.value == 'm' : 
            return dt + datetime.timedelta(minutes=value)
        if unit.value == 'h' : 
            return dt + datetime.timedelta(hours=value)
        if unit.value == 'D' : 
            return dt + datetime.timedelta(days=value)
        if unit.value == 'W' : 
            return dt + datetime.timedelta(days=value*7)
        day = dt.day
        while True:
            year = dt.year
            try:
                if unit.value == 'M' : 
                    m = dt.month + value
                    while m > 12: 
                        m -= 12
                        year += 1
                    while m < 1: 
                        m += 12
                        year -= 1
                    return dt.replace(month=m,day=day,year=year)
                if unit.value == 'Y' : 
                    return dt.replace(month=dt.year + value,day=day)
                raise Exception("Invalid DurationUnit %s" % unit)
            except ValueError:
                if day > 28:
                    day -= 1
                else:
                    raise
    
    
    
add = DurationUnit.add_item
add('s', _('seconds'),alias='seconds')
add('m', _('minutes'),alias='minutes')
add('h', _('hours')  ,alias='hours'  )
add('D', _('days')   ,alias='days'   )
add('W', _('weeks')  ,alias='weeks'  )
add('M', _('months') ,alias='months' )
add('Y', _('years')  ,alias='years'  )



