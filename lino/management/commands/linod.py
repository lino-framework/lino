# -*- coding: UTF-8 -*-
# Copyright 2016-2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import time
from django.conf import settings

from django.core.management.base import BaseCommand
# import lino
from lino.api import dd

# For the schedule logger we set level to WARNING because
# otherwise it would log a message every 10 seconds when
# running an "often" job. We must do this after Django's
# logger configuration.
# import logging
# logging.getLogger('schedule').setLevel(logging.WARNING)


class Command(BaseCommand):
    help = """Run a Lino daemon for this site."""

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            '--list', '-l', action='store_true',
            dest='list_jobs', default=False,
            help="Just list the jobs, don't run them.")

    def handle(self, *args, **options):
        # lino.startup()
        # lino.site_startup()
        # # rt.startup()
        # schedule.logger.setLevel(logging.WARNING)
        if not settings.SITE.use_linod:
            dd.logger.info("This site does not use linod.")
            return
        import schedule
        n = len(schedule.jobs)
        if n == 0:
            dd.logger.info("This site has no scheduled jobs.")
            return
        dd.logger.info("%d scheduled jobs:", n)
        for i, job in enumerate(schedule.jobs, 1):
            dd.logger.info("[%d] %r", i, job)
        if options['list_jobs']:
            return
        while True:
            schedule.run_pending()
            time.sleep(1)
