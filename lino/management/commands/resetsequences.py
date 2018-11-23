# -*- coding: UTF-8 -*-
# Copyright 2017 by Rumma & Ko Ltd.
# License: BSD, see LICENSE for more details.

""".. management_command:: resetsequences

Reset the database sequences for all plugins.

This is required (and automatically called) on a postgres after
restoring from a snapshot (:xfile:`restore.py`) because this operation
specifies explicit primary keys.

Unlike Django's :manage:`sqlsequencereset` command this does not just
output the SQL statements, it also executes them.  And it works always
on all plugins so you don't need to specify their names. 

This is functionally equivalent to the following::

  python manage.py sqlsequencereset APP1 APP2... | python manage.py shell

On SQLite or MySQL this command does nothing.

In PostgreSQL, Sequence objects are special single-row tables created
with CREATE SEQUENCE. Sequence objects are commonly used to generate
unique identifiers for rows of a table (exceprt from `PostgreSQL docs
<https://www.postgresql.org/docs/current/static/functions-sequence.html>`__).

See :blogref:`20170907`, :blogref:`20170930`.

"""

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
