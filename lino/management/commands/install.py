# -*- coding: UTF-8 -*-
# Copyright 2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

""".. management_command:: install

Runs 'pip install --upgrade' for all requirements.

Options:

.. option:: -l, --list

    Don't actually install, just print a list of the requirements to stdout.

.. option:: --noinput

    Do not prompt for user input of any kind.


.. management_command:: configure

    Old name for :manage:`install`.


"""

import subprocess
from rstgen.utils import confirm
from django.core.management.base import BaseCommand
from django.conf import settings


def runcmd(cmd, **kw):  # same code as in getlino.py
    """Run the cmd similar as os.system(), but stop when Ctrl-C."""
    # kw.update(stdout=subprocess.PIPE)
    # kw.update(stderr=subprocess.STDOUT)
    kw.update(shell=True)
    kw.update(universal_newlines=True)
    kw.update(check=True)
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
        reqs = set(settings.SITE.get_requirements())
        if len(reqs) == 0:
            print("No requirements")
        else:
            reqs = sorted(reqs)
            if options['list']:
                print('\n'.join(reqs))
                return
            runcmd('pip install --upgrade pip')
            # cmd = "pip install --upgrade --trusted-host svn.forge.pallavi.be {}".format(' '.join(reqs))
            cmd = "pip install --upgrade {}".format(' '.join(reqs))
            if not options['interactive'] or confirm("{} (y/n) ?".format(cmd)):
                runcmd(cmd)
