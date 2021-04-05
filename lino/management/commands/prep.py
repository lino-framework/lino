# -*- coding: UTF-8 -*-
# Copyright 2013-2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.conf import settings
from django.db import DEFAULT_DB_ALIAS
from lino.management.commands.initdb import Command as BaseCommand
from lino.management.commands.initdb import CommandError


class Command(BaseCommand):
    help = "Flush the database and load the default demo fixtures."

    def handle(self, *args, **options):
        fixtures = options.get('fixtures', args)
        if len(fixtures) > 0:
            raise CommandError(
                "This command takes no arguments (got %r)" % fixtures)

        if settings.SITE.readonly:
            settings.SITE.logger.info(
                "Skipped `initdb` on readonly site '%s'.",
                settings.SETTINGS_MODULE)
            return

        args = settings.SITE.demo_fixtures
        if isinstance(args, str):
            args = args.split()
        options['fixtures'] = args
        # super(Command, self).handle(*args, **options)
        super(Command, self).handle(**options)
