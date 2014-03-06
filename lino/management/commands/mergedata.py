# -*- coding: UTF-8 -*-
# Copyright 2014 Luc Saffre
# This file is part of the Lino project.
# Lino is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public License
# along with Lino; if not, see <http://www.gnu.org/licenses/>.

"""

"""

from __future__ import print_function
from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils.importlib import import_module


class Command(BaseCommand):
    help = __doc__
    args = "action_spec [args ...]"

    option_list = BaseCommand.option_list + (
        make_option('--noinput', action='store_false',
                    dest='interactive', default=True,
                    help='Do not prompt for input of any kind.'),
        make_option('--nochange', action='store_true',
                    dest='nochange', default=False,
                    help='Dry run. Do not actually change anything.'),
    )

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


