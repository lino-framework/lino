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

Default data for `pages` is the content defined in 
:mod:`lino.modlib.pages.fixtures.web`.

"""
#~ from lino.modlib.pages.fixtures.web import objects

def objects():
    
    from lino.modlib.pages.fixtures.intro import objects
    yield objects()
    
    #~ from lino.modlib.pages.fixtures.man import objects
    #~ yield objects()
    
    