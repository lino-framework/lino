# -*- coding: UTF-8 -*-
# Copyright 2016-2018 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from __future__ import unicode_literals, print_function

from django.conf import settings
from django.core.management.base import BaseCommand

from lino.api import rt


class Command(BaseCommand):
    args = "[app1.Model1] [app2.Model2] ..."
    help = """

    Update the summary tables.

    If no arguments are given, run it on all summaries.

    Otherwise (not yet implemented) every positional argument is
    expected to be a model name in the form `app_label.ModelName`, and
    only these models are being updated.

    """

    def handle(self, *args, **options):
        ses = rt.login()
        ses.run(settings.SITE.site_config.check_all_summaries)
        # checksummaries(args=args)
