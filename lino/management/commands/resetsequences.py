# -*- coding: UTF-8 -*-
# Copyright 2017-2021 Rumma & Ko Ltd.
# License: GNU Affero General Public License v3 (see file COPYING for details)


from django.core.management.base import BaseCommand
from django.core.management.color import no_style
from django.db import connections, DEFAULT_DB_ALIAS

from lino.core.utils import get_models


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--database', action='store', dest='database',
                            default=DEFAULT_DB_ALIAS,
                            help='Nominates a database to reset. '
                                 'Defaults to the "default" database.')

    def handle(self, *args, **options):
        using = options.get('database', DEFAULT_DB_ALIAS)
        conn = connections[using]
        lst = get_models(include_auto_created=True)
        cursor = conn.cursor()
        for sql in conn.ops.sequence_reset_sql(no_style(), lst):
            cursor.execute(sql)
