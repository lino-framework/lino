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
Execute the Python script(s) specified as command-line arguments
after having set up the Django environment.

For example if you have a file `tmp.py` with the following content...

::

  from lino.modlib.contacts.models import Partner
  print Partner.objects.all()

... then you can run this script using::

  $ python manage.py run tmp.py
  [<Partner: Rumma & Ko OÜ>, ...  <Partner: Charlier Ulrike>, 
  '...(remaining elements truncated)...']
  

This is almost the same as redirecting stdin of Django's ``shell`` command 
(i.e. doing ``python manage.py shell < tmp.py``), but without the disturbing 
messages from the interactive console::

  Python 2.7.1 (r271:86832, Nov 27 2010, 18:30:46) [MSC v.1500 32 bit (Intel)] on win32
  Type "help", "copyright", "credits" or "license" for more information.
  (InteractiveConsole)
  >>> >>> [<Partner: Rumma & Ko OÜ>, ...  <Partner: Charlier Ulrike>, 
  '...(remaining elements truncated)...']
  >>>
  

This is another possible answer to a frequently asked Django question 
(`[1] <http://stackoverflow.com/questions/4847469/use-django-from-python-manage-py-shell-to-python-script>`__,
`[2] <http://www.b-list.org/weblog/2007/sep/22/standalone-django-scripts/>`__).

And it is a very simple solution. 
See the source code at :srcref:`/lino/management/commands/run.py`.

"""

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = __doc__
    args = "file1 [file2 ...]"
    
    def handle(self, *args, **options):
        for arg in args:
            execfile(arg)
          
