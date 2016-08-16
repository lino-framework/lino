# -*- coding: UTF-8 -*-
# Copyright 2013-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""

.. management_command:: initdb_demo

Calls :manage:`initdb` using the application's
:attr:`lino.core.site.Site.demo_fixtures`.

Introduction see :ref:`lino.tutorial.hello`.

"""
from past.builtins import basestring

from django.conf import settings
from django.db import DEFAULT_DB_ALIAS
from lino.modlib.lino_startup.management.commands.initdb import Command as BaseCommand
from lino.modlib.lino_startup.management.commands.initdb import CommandError


class Command(BaseCommand):
    help = __doc__

    def add_arguments(self, parser):
        parser.add_argument('--noinput', action='store_false',
                            dest='interactive', default=True,
                            help='Do not prompt for input of any kind.'),
        parser.add_argument('--database', action='store', dest='database',
                            default=DEFAULT_DB_ALIAS,
                            help='Nominates a database to reset. '
                                 'Defaults to the "default" database.')

    def handle(self, *args, **options):
        if len(args) > 0:
            raise CommandError(
                "This command takes no arguments (got %r)" % args)

        args = settings.SITE.demo_fixtures
        if isinstance(args, basestring):
            args = args.split()
        super(Command, self).handle(*args, **options)
