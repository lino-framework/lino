## Copyright 2009 Luc Saffre

## This file is part of the Lino project.

## Lino is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## Lino is distributed in the hope that it will be useful, but WITHOUT
## ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
## or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
## License for more details.

## You should have received a copy of the GNU General Public License
## along with Lino; if not, write to the Free Software Foundation,
## Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

from lino.django.tom.menus import Menu

menu = Menu(None,"main","Main Menu")

#~ class TomSite(MenuContainer):
    #~ def __init__(self):
        #~ #self._registry={}
        #~ MenuContainer.__init__(self)
        
    #~ def register(self,rptclass):
        #~ self._registry[rptclass.__name__] = rptclass
        
    #~ def get_report(self,name):
        #~ return self._registry[name]()
        
#~ site = TomSite()
