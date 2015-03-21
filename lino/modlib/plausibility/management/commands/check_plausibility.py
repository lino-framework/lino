# -*- coding: UTF-8 -*-
# Copyright 2015 by Luc Saffre.
# License: BSD, see LICENSE for more details.
"""Defines the :manage:`check_plausibility` management command.

.. management_command:: check_plausibility

.. py2rst::

  from lino.modlib.plausibility.management.commands.check_plausibility \
      import Command
  print(Command.help)

"""

from __future__ import unicode_literals, print_function

from optparse import make_option
from django.core.management.base import BaseCommand
from lino.modlib.plausibility.models import check_plausibility
from lino.modlib.plausibility.choicelists import Checkers


class Command(BaseCommand):
    args = "[app1.Model1.Checker1] [app2.Model2.Checker2] ..."
    help = """

    Update the table of plausibility problems.

    If no arguments are given, run it on all plausibility checkers.
    Otherwise every positional argument is expected to be a model name in
    the form `app_label.ModelName`, and only these models are being
    updated.

    """

    option_list = BaseCommand.option_list + (
        make_option(
            '-l', '--list', action='store_true', dest='list',
            default=False,
            help="Don't check, just show a list of available checkers."),
        make_option(
            '-f', '--fix', action='store_true', dest='fix',
            default=False,
            help="Fix any repairable problems."),
    )

    def handle(self, *args, **options):
        if options['list']:
            Checkers.show()
        else:
            check_plausibility(args=args, fix=options['fix'])
