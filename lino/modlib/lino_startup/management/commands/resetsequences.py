# -*- coding: UTF-8 -*-
# Copyright 2017 by Luc Saffre.
# License: BSD, see LICENSE for more details.

""".. management_command:: resetsequences

postgres requires us to reset the "sequences" after restoring from a
snapshot because this operation specifies explicit primary keys. See
:blogref:`20170907`.

You might do this using::

  python manage.py sqlsequencereset APP1 APP2... | python manage.py shell

But it is difficult to specify all plugins as arguments. So I created
a variant which is more admin-friendly, the :manage:`resetsequences`
command.

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
