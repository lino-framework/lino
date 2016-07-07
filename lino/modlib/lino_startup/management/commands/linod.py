# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
# License: BSD, see file LICENSE for more details.

"""This defines the :manage:`linod` management command.

.. management_command:: linod

Starts a daemon that runs scheduled background tasks.

On a development machine you simply run this in a separate
terminal. On a production server this should be installed as a service
(starting a new process every 10 seconds would probably cause a big
server load).

Before using this command you must manually install the `schedule
<https://github.com/dbader/schedule>`__ package::

  $ pip install schedule

"""

from __future__ import print_function

import time
import schedule

from lino.utils import dblogger
from lino.utils.daemoncommand import DaemonCommand


class Command(DaemonCommand):

    # preserve_loggers = (logger,dblogger.logger)
    preserve_loggers = [dblogger.logger]

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            '--list', '-l', action='store_true',
            dest='list_jobs', default=False,
            help="List all jobs to stdout")

    def handle(self, *args, **options):
        if options['list_jobs']:
            for i, job in enumerate(schedule.jobs):
                print(i, job)
            return
        while True:
            schedule.run_pending()
            time.sleep(1)

