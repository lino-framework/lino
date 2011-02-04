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


class Column(object):
    def __init__(self,index,header,width=None):
        self.header = header
        self.width = width
        self.index = index
        
    def adjust_width(self,row):
        s = unicode(row[self.index])
        if self.width is None or self.width < len(s):
            self.width = len(s)

def html2rst(s):
    s = s.replace('<b>','**')
    s = s.replace('</b>','**')
    return s
    
def write_header(fd,level,s):
    def writeln(s=''):
        fd.write(s+'\n')
        
    #~ writeln()
    if level == 1:
        writeln('=' * len(s))
    elif level == 2:
        writeln('-' * len(s))
    writeln(s)
    if level == 1:
        writeln('=' * len(s))
    elif level == 2:
        writeln('-' * len(s))
    elif level == 3:
        writeln('=' * len(s))
    elif level == 4:
        writeln('-' * len(s))
    else:
        raise Exception("Invalid level %d" % level)
    writeln()

class SimpleTable(object):
    def __init__(self,headers):
        self.headers = headers
        self.cols = [ Column(i,h) for i,h in enumerate(headers)]
        self.adjust_widths(headers)
        
    def adjust_widths(self,row):
        for col in self.cols:
            col.adjust_width(row)
      
    def format_row(self,row):
        return ' '.join([unicode(row[c.index]).ljust(c.width) for c in self.cols])
        
    def write(self,fd,rows):
        def writeln(s):
            fd.write(s+'\n')
            
        for row in rows: self.adjust_widths(row)
        writeln(' '.join([('=' * c.width) for c in self.cols]))
        writeln(self.format_row(self.headers))
        writeln(' '.join([('=' * c.width) for c in self.cols]))
        for row in rows:
            writeln(self.format_row(row))
        writeln(' '.join([('=' * c.width) for c in self.cols]))
    