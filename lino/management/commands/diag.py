# -*- coding: UTF-8 -*-
# Copyright 2012-2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

""".. management_command:: diag

Writes a diagnostic status report about this Site.

This is a command-line shortcut for calling
:meth:`lino.core.site.Site.diagnostic_report_rst`.

"""

from __future__ import print_function

import six

from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = __doc__

    def handle(self, *args, **options):
        if six.PY2:
            encoding = self.stdout.encoding or 'utf-8'

            def writeln(ln=''):
                self.stdout.write(ln.encode(encoding, "xmlcharrefreplace") + "\n")

        else:
            def writeln(ln=''):
                self.stdout.write(ln + "\n")

        settings.SITE.startup()
        writeln(settings.SITE.diagnostic_report_rst(*args))


