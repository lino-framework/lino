# -*- coding: UTF-8 -*-
# Copyright 2014-2017 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

""".. management_command:: recmail

``recmail`` stands for "receive mail". Starts a configurable SMTP
server which forwards incoming mails to your Lino application. For
every incoming mail it sends a `mail_received` signal.  It is up to
your application to decide what to with these mails.

If you want to run this as a daemon, you must do::

  $ pip install python-daemon

"""

from os.path import join

import smtpd
import asyncore

from django.conf import settings
from django.core.management.base import CommandError
from lino.utils import dblogger
from lino.utils.daemoncommand import DaemonCommand

from lino.modlib.smtpd.signals import mail_received


class MySMTPServer(smtpd.SMTPServer):
    
    def process_message(self, peer, mailfrom, rcpttos, data):
        rv = mail_received.send(
            self, peer=peer, mailfrom=mailfrom, rcpttos=rcpttos, data=data)
        dblogger.info("20140703 process_message %s", rv)


# DEFAULT_PORT = 25
DEFAULT_PORT = 1025


def main(*args, **options):
    if len(args) == 0:
            addr, port = '127.0.0.1', DEFAULT_PORT
    elif len(args) != 1:
        raise CommandError(
            'Must specify ADDR or ADDR:PORT as argument')
    else:
        a = args[0].split(':')
        if len(a) == 2:
            addr, port = a
            port = int(port)
        elif len(a) == 1:
            addr = a[0]
            port = DEFAULT_PORT
        else:
            raise CommandError("Invalid ADDR, must be something "
                               "like 127.0.0.1 or 127.0.0.1:1025")
    settings.SITE.startup()
    MySMTPServer((addr, port), None)
    dblogger.info("20140703 start listening on %s:%d", addr, port)
    asyncore.loop()
    dblogger.info("20140703 stopped listening on %s:%d", addr, port)


class Command(DaemonCommand):
    
    help = "Starts a configurable SMTP server which forwards " \
           "incoming mails to your Lino application"

    preserve_loggers = [dblogger.logger]

    stdout = join(settings.SITE.project_dir, 'recmail', 'out.log')
    stderr = join(settings.SITE.project_dir, 'recmail', 'err.log')
    pidfile = join(settings.SITE.project_dir, 'recmail', 'pid')

    def handle(self, *args, **options):
        main(*args, **options)
