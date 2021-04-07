# -*- coding: UTF-8 -*-
# Copyright 2012-2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from past.builtins import execfile

import sys
import argparse

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):

    help = """Run a Python script within the Django environment for this site."""

    requires_system_checks = False

    def add_arguments(self, parser):
        parser.add_argument('filename', nargs=argparse.REMAINDER,
                            help='The script to run.')
        # parser.description = """Execute a standalone Python script after
        # having set up the Django environment."""

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
