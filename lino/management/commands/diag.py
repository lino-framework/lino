# -*- coding: UTF-8 -*-
# Copyright 2012-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
.. management_command:: diag

Writes a diagnostic status report about this Site.
"""

from __future__ import print_function

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


class Command(BaseCommand):
    help = __doc__
    args = "output_dir"

    def handle(self, *args, **options):
        if args:
            raise CommandError("This command doesn't accept any arguments.")

        encoding = self.stdout.encoding or 'utf-8'

        def writeln(ln=''):
            self.stdout.write(ln.encode(encoding, "xmlcharrefreplace") + "\n")

        settings.SITE.startup()
        # writeln(settings.SITE.get_db_overview_rst())
        writeln(settings.SITE.diagnostic_report_rst())


