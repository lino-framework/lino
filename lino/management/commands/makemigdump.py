# -*- coding: UTF-8 -*-
# Copyright 2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""
.. management_command:: makemigdump

Create a dump for migration tests.

Calls :manage:`dump2py` to create python dump in a
`tests/dumps/<version>` directory


See :doc:`/dev/migtests`
"""
import six

from django.conf import settings
from django.db import DEFAULT_DB_ALIAS
from lino.management.commands.initdb import Command as BaseCommand
from lino.management.commands.initdb import CommandError


class Command(BaseCommand):
    """Create a dump for migration tests.
    """

    def handle(self, *args, **options):


          # : loop through all demo projects.
          # skip if the project has no  :xfile:`test_restore.py` file.
          # dumpdir = "tests/dumps/" + version
          # python manage.py dump2py dumpdir
          # error if 

        
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
