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

import cgi
def LIST(tag,items):
    s = '\n'.join(['<li>%s</li>' % cgi.escape(unicode(i)) for i in items])
    return "<%s>%s</%s>" % (tag,s,tag)
def UL(items): return LIST('UL',items)
def OL(items): return LIST('OL',items)

