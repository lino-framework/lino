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

from __future__ import unicode_literals

from lino.modlib.codechanges.models import change, issue

change(20121222,"experimental","""
Documenting code changes
------------------------
The new module :mod:`lino.modlib.codechanges` is an attempt 
to make it easier to write code change reports, 
and to find them back when needed.
:menuselection:`Explorer --> System --> Code Changes`
currently displays a list of all changes.
""")

issue(20121222,"missing feature","""
It seems that `detail_layout` doesn't work on `VirtualTable`.
""")
    
