# -*- coding: UTF-8 -*-
## Copyright 2011-2012 Luc Saffre
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

For backward compatibility when loading dumpy fixtures 
created by a lino.apps.pcsw before 1.4.4.

Will be removed when the last known user has migrated.


These fixtures contain the following lines at the end::

  from lino.apps.dsbe.migrate import install
  install(globals())

"""

from django.conf import settings

def install(globals_dict):
    settings.LINO.install_migrations(globals_dict)

