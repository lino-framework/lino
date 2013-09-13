# -*- coding: UTF-8 -*-
## Copyright 2013 Luc Saffre
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
Used by :class:`lino.utils.appy_pod.PrintLabelsAction` and 
:mod:`lino.modlib.contacts`.

"""

from __future__ import print_function

from lino.utils import join_elems
from lino.utils.xmlgen.html import E

class Addressable(object):
    """
    Interface (abstract base class) to encapsulates the generating 
    of "traditional" ("snail") mail addresses.
    It differentiates between the "person" and the "location" part 
    of an address.
    
    Mr. Luc Saffre     | person
    Rumma & Ko OÜ      | person
    Uus 1              | location
    Vana-Vigala küla   | location
    ...                | location
    
    """
    
    def address_person_lines(self):
        """
        Expected to yield one or more unicode strings, one for each line
        of the person part.
        """
        raise NotImplementedError()
        
    def address_location_lines(self):
        """
        Expected to yield one or more unicode strings, one for each line
        of the location part.
        """
        raise NotImplementedError()
        
    def address_lines(self):
        for ln in self.address_person_lines() : yield ln
        for ln in self.address_location_lines() : yield ln
        
    
    def get_address(self,linesep="\n"):
        """
        The plain text full postal address (person and location). 
        Lines are separated by `linesep`.
        """
        #~ return linesep.join(self.address_lines())
        return linesep.join(list(self.address_person_lines()) + list(self.address_location_lines()))
    address = property(get_address)
          
    def get_address_html(self,**attrs):
        """
        Returns the full postal address a a string containing html 
        markup of style::
        
            <p>line1<br />line2...</p>
          
        Optional attributes for the enclosing `<p>` tag can be 
        specified as keyword arguments. Example::
        
            >>> class MyAddr(Addressable):
            ...     def __init__(self,*lines): self.lines = lines
            ...     def address_person_lines(self): return []
            ...     def address_location_lines(self): return self.lines
            ...     
            >>> addr = MyAddr('line1','line2')
            >>> print(addr.get_address_html(class_="Recipient"))
            <p class="Recipient">line1<br />line2</p>
          
        See :mod:`lino.utils.xmlgen.html`.
          
        """
        lines = join_elems(self.address_lines(),E.br)
        return E.tostring(E.p(*lines,**attrs))
        
    address_html = property(get_address_html)
    """
    A property which calls :meth:`get_address_html`.
    """
    
