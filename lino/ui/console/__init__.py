## Copyright 2009-2010 Luc Saffre
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

from lino.ui import base
from lino.ui.console import renderers_text

class Panel:
    pass
    
class Element:
    def __init__(self,*args,**kw):
        self.args = args
        self.kw = kw

class FieldElement(Element):
    def __init__(self,field,*args,**kw):
        self.field = field
        Element.__init__(self,*args,**kw)

class MethodElement(Element):
    def __init__(self,field,*args,**kw):
        self.field = field
        Element.__init__(self,*args,**kw)

class ConsoleUI(base.UI):
  
    GridElement = Element
    VirtualFieldElement = Element
    MethodElement = Element
    ButtonElement = Element
    Panel = Panel
    Store = Element
    Spacer = Element
    StaticTextElement = Element
    InputElement = Element
  
    def main_panel_class(self,layout):
        return Panel
    def report_as_text(self,rpt):
        rh = self.get_report_handle(rpt)
        rr = renderers_text.TextReportRequest(rh,*args,**kw)
        return rr.render()
   
ui = ConsoleUI()