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
Set password "1234" for all users.

This is an additive fixture designed to work also on existing data::

  T:\data\luc\lino_local\dsbe>python manage.py loaddata demo2
  INFO Analyzing models...
  INFO Loading t:\hgwork\lino\lino\modlib\users\fixtures\demo2.py...
  Installed 8 object(s) from 1 fixture(s)



"""

from django.conf import settings

def objects():
    for u in settings.LINO.user_model.objects.exclude(profile=''):
        u.set_password('1234')
        yield u
                
