# -*- coding: UTF-8 -*-
# Copyright 2012-2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = __doc__

    def handle(self, *args, **options):
        def writeln(ln=''):
            self.stdout.write(ln + "\n")

        settings.SITE.startup()
        writeln(settings.SITE.diagnostic_report_rst(*args))
