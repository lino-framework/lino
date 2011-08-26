## Copyright 2009-2011 Luc Saffre
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

"""The default URLconf module, 
pointed to by
:setting:`ROOT_URLCONF` in :mod:`lino.apps.std.settings`.
"""

#~ import os
#~ import sys
#~ from django.conf import settings
#~ from django.conf.urls.defaults import patterns, include, url

from lino.ui.extjs3 import UI

# install Lino urls under root location (`/`)
urlpatterns = UI().get_patterns()
