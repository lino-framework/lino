## Copyright 2009-2013 Luc Saffre
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
The default URLconf module, defines the variable `urlpatterns` 
as required by Django.
Application code doesn't need to worry about this.

This is found by Django because 
:mod:`lino.projects.std.settings`
:setting:`ROOT_URLCONF` 
is set to ``'lino.ui.extjs3.urls'``.

"""

from django.conf import settings
urlpatterns = settings.SITE.get_patterns()
