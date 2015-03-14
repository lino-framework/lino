# -*- coding: UTF-8 -*-
# Copyright 2015 by Luc Saffre.
# License: BSD, see LICENSE for more details.
""".. management_command:: repairdata

Run automatic reparation on all repairable database rows.

See :mod:`lino.mixins.repairable`.

"""

from __future__ import unicode_literals, print_function

import sys
from optparse import make_option
from django.core.management.base import BaseCommand
from lino.api import dd
from lino.mixins.repairable import repairdata

REQUEST = dd.PseudoRequest("repairdata")


class Command(BaseCommand):
    help = __doc__

    option_list = BaseCommand.option_list + (
        make_option(
            '-r', '--really', action='store_true', dest='really',
            default=False,
            help="If this is not specified, we just show repairable "
            "problems without actually repairing anything."),
    )

    def handle(self, *args, **options):
        n = 0
        for msg in repairdata(args, really=options['really']):
            print(msg)
            n += 1
        if n > 0:
            print("Found {0} repairable problem(s).".format(n))
            sys.exit(-1)
