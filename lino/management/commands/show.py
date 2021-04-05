# -*- coding: UTF-8 -*-
# Copyright 2013-2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import argparse

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Show the content of a specified table to standard output."
    # args = "action_spec [options] [args ...]"

    def add_arguments(self, parser):
        parser.add_argument('-u', '--username', action='store', dest='username',
                            default=None,
                            help='The username to act as. Default is `None`.'),
        parser.add_argument('-l', '--language', action='store', dest='language',
                            help="The language to use. "
                                 "Default is the site's default language.")
        parser.add_argument('action_spec',
                            help='The table to show.')

    def handle(self, *args, **options):
        if True:  # Django 1.10
            # spec = options['action_spec'][0]
            spec = options['action_spec']
        else:
            if len(args) == 0:
                raise CommandError("I need at least one argument.")
            spec = args[0]

        username = options['username']
        ses = settings.SITE.login(username)

        ses.show(spec, language=options['language'])
