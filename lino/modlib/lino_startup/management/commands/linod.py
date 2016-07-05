# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
# License: BSD, see file LICENSE for more details.

""".. management_command:: linod

Starts a daemon that runs scheduled background tasks.

On a development machine you simply run this in a separate
terminal. On a production server this should be installed as a service
(starting a new process every 10 seconds would probably cause a big
server load).

"""

import time
import schedule

from lino.utils import dblogger
from lino.utils.daemoncommand import DaemonCommand


class Command(DaemonCommand):

    # stdout = '/var/log/lino/watch_tim.log'
    # stdout = os.path.join(settings.PROJECT_DIR, "watch_tim","stdout.log")
    # stderr = '/var/log/lino/watch_tim.errors.log'
    # os.path.join(settings.PROJECT_DIR, "watch_tim","errors.log")
    # pidfile = os.path.join(settings.PROJECT_DIR, "watch_tim","pid")
    # pidfile = '/var/run/watch_tim.pid' # os.path.j

    # preserve_loggers = (logger,dblogger.logger)
    preserve_loggers = [dblogger.logger]

    def handle(self, *args, **options):
        while True:
            schedule.run_pending()
            time.sleep(1)

