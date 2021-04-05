# -*- coding: UTF-8 -*-
# Copyright 2014 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)


import logging
logger = logging.getLogger(__name__)

from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from importlib import import_module


class Command(BaseCommand):
    help = "Work in process"
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
