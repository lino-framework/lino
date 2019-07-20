# -*- coding: UTF-8 -*-
# Copyright 2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

""".. management_command:: configure

Runs 'pip install' for all requirements.

Options:

.. option:: --noinstall
.. option:: --noinput

    Do not prompt for user input of any kind.


TODO: options for just displaying them,

"""

from __future__ import print_function

import subprocess

from django.core.management.base import BaseCommand
from django.conf import settings


def runcmd(cmd, **kw):  # same code as in getlino.py
    """Run the cmd similar as os.system(), but stop when Ctrl-C."""
    # kw.update(stdout=subprocess.PIPE)
    # kw.update(stderr=subprocess.STDOUT)
    kw.update(shell=True)
    kw.update(universal_newlines=True)
    # subprocess.check_output(cmd, **kw)
    subprocess.run(cmd, **kw)
    # os.system(cmd)


class Command(BaseCommand):
    help = __doc__

    requires_system_checks = False

    def add_arguments(self, parser):
        parser.add_argument('--noinput', action='store_false',
                            dest='interactive', default=True,
                            help='Do not prompt for input of any kind.')
        parser.add_argument('-l', '--list', action='store_true',
                            dest='list', default=False,
                            help="Just list the requirements, don't install them.")

    def handle(self, *args, **options):
        lst = options['list']
        for r in settings.SITE.get_requirements():
            if lst:
                print(r)
            else:
                runcmd("pip install --upgrade " + r)


