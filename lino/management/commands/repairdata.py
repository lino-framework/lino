# -*- coding: UTF-8 -*-
# Copyright 2015 by Luc Saffre.
# License: BSD, see LICENSE for more details.
""".. management_command:: repairdata

Run automatic reparation on repairable database rows.

If no arguments are given, run it on all repairable models.  Otherwise
every positional argument is expected to be a model name in the form
`app_label.ModelName`, and only these models are being tested.

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
    args = "[app1.Model1] [app2.Model2] ..."
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
            try:
                print(msg)
            except UnicodeEncodeError as e:
                raise Exception("%s while rendering %r" % (e, msg))
            n += 1
        if n > 0:
            print("Found {0} repairable problem(s).".format(n))
            sys.exit(-1)
