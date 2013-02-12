## Copyright 2013 Luc Saffre
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
The :mod:`lino.runtime` module 
provides a stable transparent API which encapsulates 
the startup internals.

Lino application developers must just know the following:
Lino needs to do certain things "at startup" 
(i.e. when the models cache has been populated).
Most application code which uses Lino features will break 
if this startup hasn't been called.
And because Django unfortunately doesn't provide 
a signal or other method to specify things that 
should be run automatically at startup, 
we need to use some tricks.

The tricks are:

- Lino comes with wrappers that "override" Django's 
  dumpdata and loaddata management commands.
  
- If Application developer write their own management commands, 
  they should use ``from lino.runtime import settings`` instead 
  of the usual ``from django.conf import settings``.

- Unlike :mod:`lino.dd`, the :mod:`lino.runtime`
  **may not** be imported at the top level of "models modules".

"""

raise Exception("No longer needed")

from django.conf import settings
#~ settings.LINO.startup()
settings.LINO.analyze_models()
