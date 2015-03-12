# -*- coding: UTF-8 -*-
# Copyright 2015 by Luc Saffre.
# License: BSD, see LICENSE for more details.
""".. management_command:: repairdata

Run automatic reparation on all repairable database rows.

See :mod:`lino.mixins.repairable`.

"""

from __future__ import unicode_literals, print_function

from optparse import make_option
from django.core.management.base import BaseCommand
from lino.api import dd
from lino.mixins.repairable import repairdata

REQUEST = dd.PseudoRequest("repairdata")


class Command(BaseCommand):
    help = __doc__

    option_list = BaseCommand.option_list + (
        make_option(
            '-s', '--simulate', action='store', dest='simulate',
            default=False,
            help="Only simulate, don't actually repair anything."),
    )

    def handle(self, *args, **options):
        for msg in repairdata(simulate=options['simulate']):
            print(msg)

