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

import datetime
from django.conf import settings
from lino.utils.instantiator import Instantiator

def objects():
    page = Instantiator('pages.Page','ref title body').build
    yield page("index","Welcome","""\
<p>
Welcome to the <b>%(site)s</b> site.
This is the "plain web content" section.
To see Lino, please go to the <a href="/admin/">admin</a> section
and then log in using the button in the upper right corner and one of the following usernames:
</p>
<ul>
<li>(German:) root, hubert, melanie, caroline</li>
<li>(French:) robert, alicia</li>
</ul>
<p>They all have "1234" as password.</p>
""" % dict(site=settings.LINO.title))