# -*- coding: UTF-8 -*-
# Copyright 2013-2017 Luc Saffre
# License: BSD (see file COPYING for details)

"""

.. management_command:: initdb_demo
.. management_command:: prep

Calls :manage:`initdb` using the application's
:attr:`lino.core.site.Site.demo_fixtures`.

Introduction see :ref:`lino.tutorial.hello`.

"""
import six

from django.conf import settings
from django.db import DEFAULT_DB_ALIAS
from lino.modlib.lino_startup.management.commands.initdb import Command as BaseCommand
from lino.modlib.lino_startup.management.commands.initdb import CommandError


class Command(BaseCommand):
    """Flushes the database and loads the default demo fixtures.
    """

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
        if isinstance(args, six.string_types):
            args = args.split()
        options['fixtures'] = args
        # super(Command, self).handle(*args, **options)
        super(Command, self).handle(**options)
