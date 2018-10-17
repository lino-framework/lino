# -*- coding: UTF-8 -*-
# Copyright 2012-2018 Rumma & Ko Ltd
# License: BSD, see LICENSE for more details.
"""
.. management_command:: run

Execute a standalone Python script after having set up the Django
environment.

``manage.py run myscript.py`` is almost the same as redirecting stdin
of Django's ``shell`` command (i.e. doing ``manage.py shell <
myscript.py``), but with the possibility of using **command line
arguments**.

For example if you have a file `myscript.py` with the following content...

::

  import sys
  from myapp.models import Partner
  print Partner.objects.get(pk=sys.args[1])

... then you can run this script using::

    $ python manage.py run myscript.py 101
    Bäckerei Ausdemwald

This command modifies `sys.args`, `__file__` and `__name__` so that
the invoked script sees them as if it had been called directly.

It is similar to the `runscript
<http://django-extensions.readthedocs.org/en/latest/runscript.html>`_
command which comes with `django-extensions
<http://django-extensions.readthedocs.org/en/latest/index.html>`__.

This is yet another answer to the frequently asked Django question
about how to run standalone Django scripts
(`[1] <http://stackoverflow.com/questions/4847469/use-django-from-python-manage-py-shell-to-python-script>`__,
`[2] <http://www.b-list.org/weblog/2007/sep/22/standalone-django-scripts/>`__).
"""

from __future__ import unicode_literals
#from six.moves.builtins import execfile
from past.builtins import execfile


import sys
import argparse

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):

    requires_system_checks = False

    def add_arguments(self, parser):
        parser.add_argument('filename', nargs=argparse.REMAINDER,
                            help='The script to run.')
        parser.description = """Execute a standalone Python script after
        having set up the Django environment."""

    def handle(self, *args, **options):
        if True:  # Django 1.10
            fn = options['filename'][0]
        else:
            if len(args) == 0:
                raise CommandError("I need at least one argument.")
            fn = args[0]
        # fn = filename[0]
        sys.argv = sys.argv[2:]
        globals()['__name__'] = '__main__'
        globals()['__file__'] = fn
        execfile(fn, globals())
