## Copyright 2008-2011 Luc Saffre
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

Implements a :mod:`contacts` application label.

The :class:`contacts.Person` and :class:`contacts.Company` 
in this implementation are 
abstract because you are probably going to extend them.
The simplest way to make them usable is to subclass them 
without any change::

  from lino.modlib.contacts import models as contacts
  
  class Person(contacts.Person):
      class Meta:
          app_label = 'contacts'
      
  class Company(contacts.Company):
      class Meta:
          app_label = 'contacts'



"""