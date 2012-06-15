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

u"""
Execute a standalone Python script after having set up the Django 
environment. Also modify `sys.args` and `__name__` so that 
the invoked script sees them as if it had been called directly.

This is yet another answer to the frequently asked Django question
about how to run standalone Django scripts
(`[1] <http://stackoverflow.com/questions/4847469/use-django-from-python-manage-py-shell-to-python-script>`__,
`[2] <http://www.b-list.org/weblog/2007/sep/22/standalone-django-scripts/>`__).
It is almost the same as redirecting stdin of Django's ``shell`` command 
(i.e. doing ``python manage.py shell < myscript.py``), but without the disturbing 
messages from the interactive console.

For example if you have a file `myscript.py` with the following content...

::

  from lino.modlib.contacts.models import Partner
  print Partner.objects.all()

... then you can run this script using::

  $ python manage.py run myscript.py
  [<Partner: Rumma & Ko OÜ>, ...  <Partner: Charlier Ulrike>, 
  '...(remaining elements truncated)...']
  
  

See the source code at :srcref:`/lino/management/commands/run.py`.

"""

import sys
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = __doc__
    args = "scriptname [args ...]"
    
    def handle(self, *args, **options):
        if len(args) == 0:
            raise CommandError("I need at least one argument.")
        fn = args[0]
        sys.argv = sys.argv[2:]
        globals()['__name__'] = '__main__'
        execfile(fn)
          
