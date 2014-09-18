# -*- coding: UTF-8 -*-
# Copyright 2013-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""

"""

from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


class Command(BaseCommand):
    help = __doc__
    args = "action_spec [args ...]"

    option_list = BaseCommand.option_list + (
        make_option(
            '--username', action='store', dest='username',
            default='root',
            help='The username to act as. Default is "root".'),
        make_option(
            '--language', action='store', dest='language',
            help="The language to use. "
            "Default is the site's default language."),
    )

    def handle(self, *args, **options):
        if len(args) == 0:
            raise CommandError("I need at least one argument.")
        #~ settings.SITE.startup()
        spec = args[0]

        username = options['username']
        ses = settings.SITE.login(username)

        ses.show(spec, language=options['language'])
