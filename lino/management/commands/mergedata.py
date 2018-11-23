# -*- coding: UTF-8 -*-
# Copyright 2014 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

""".. management_command:: mergedata

Takes the full name of a python module as argument. It then imports
this module and expects it to define a function `objects` in its
global namespace. It calls this function and expects it to yield a
series of Django instance objects which have not yet been saved. It
then compares these objects with the "corresponding data" in the
database and prints a summary to stdout. It then suggests to merge the
new data into the database.

- It never *deletes* any stored records.
- All incoming objects either replace an existing (stored) object, or
  will be added to the database.
- If an incoming object has a non-empty primary key, then it replaces
  the corresponding stored object. Otherwise, if the model has
  `unique` fields, then these cause potential replacement.

Currently the command is only partly implemented, it doesn't yet
update existing records.  But it detects whether records are new, and
adds only those.

"""

from __future__ import print_function
from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from importlib import import_module


class Command(BaseCommand):
    help = __doc__
    args = "action_spec [args ...]"

    def add_arguments(self, parser):
        parser.add_argument(
            '--noinput', action='store_false',
            dest='interactive', default=True,
            help='Do not prompt for input of any kind.')
        parser.add_argument(
            '--nochange', action='store_true',
            dest='nochange', default=False,
            help='Dry run. Do not actually change anything.')

    def merge_module(self, name):
        m = import_module(name)
        
        for obj in m.objects():
            M = obj.__class__
            if obj.pk is None:
                stored = set()
                for f in obj._meta.fields:
                    if not f.primary_key and f.unique:
                        v = getattr(obj, f.name)
                        fkw = {f.name: v}
                        try:
                            o2 = M.objects.get(**fkw)
                            stored.add(o2)
                            logger.debug("Found %s with %s=%s", o2, f.name, v)
                        except M.DoesNotExist:
                            pass  # ok

                if len(stored) == 0:
                    obj.full_clean()
                    if not self.nochange:
                        obj.save()
                        tpl = 'New %s %s has been created.'
                    else:
                        tpl = 'New %s %s would have been created.'
                    logger.info(tpl, M._meta.verbose_name, obj)
                elif len(stored) == 1:
                    logger.info("Cannot yet update existing %s", obj)
                else:
                    logger.info("Found %d existing rows for %s",
                                len(stored), obj)
            else:
                logger.warning("Ignored non-empty primary key %s", obj)

    def handle(self, *args, **options):
        if len(args) == 0:
            raise CommandError("I need at least one argument.")

        self.nochange = options['nochange']
        self.interactive = options['interactive']

        for name in args:
            self.merge_module(name)


