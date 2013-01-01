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

Deserves documentation.

"""

from __future__ import unicode_literals

#~ blogger = Blogger(username='luc')
from lino.modlib.tickets.blogger import Blogger
blogger = Blogger()
blogger.set_user('robin')

LINO = blogger.project("lino","Public relations","""
""",
srcref_url_template='http://code.google.com/p/lino/source/browse%s',
changeset_url_template='http://code.google.com/p/lino/source/detail?r=%s')

blogger.set_project(LINO)

blogger.project("lino.pr","Public relations","""
Long-term project. 
This is when I work on improving the first impression.
""",parent=LINO)
blogger.project("lino.dev","Development process","""
Release cycle, documentat
""",parent=LINO)
blogger.project("lino.cms","Content management","""
""",parent=LINO)
blogger.project("lino.core","Core functionality","""
""")
blogger.project("lino.cosi","Lino Cosi first prototype ","""
""")


blogger.milestone('1.4.3',20120328)
blogger.milestone('1.4.5',20120716)
blogger.milestone('1.4.7',20120717)
blogger.milestone('1.4.8',20120722)
blogger.milestone('1.4.9',20120729)
blogger.milestone('1.5.3',20121208)

