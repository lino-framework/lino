# -*- coding: UTF-8 -*-
# Copyright 2012 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Writes a status report about this Site.
Used to monitor a production database.
"""
# from future import standard_library
# standard_library.install_aliases()

import logging
logger = logging.getLogger(__name__)

import os
import errno
import pickle as pickle
import sys
from optparse import make_option
from os.path import join

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.utils.encoding import force_text
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

from django.db import connections, transaction
from django.core.exceptions import ImproperlyConfigured
from django.db.utils import DEFAULT_DB_ALIAS

from django.db.backends.sqlite3.base import DatabaseWrapper as sqlite
try:
    from django.db.backends.mysql.base import DatabaseWrapper as mysql
except ImproperlyConfigured:
    mysql = None


import lino
import rstgen
from lino.core.utils import obj2str, full_model_name, sorted_models_list


def diffs(old, new, prefix=''):
    if type(old) != dict:
        if old != new:
            yield "%s : %s -> %s" % (prefix, old, new)
        return
    keys = set(list(old.keys()) + list(new.keys()))
    keys.discard('timestamp')
    #~ diffs = []
    if prefix:
        prefix += ' '
    for k in keys:
        ov = old.get(k)
        nv = new.get(k)
        if ov != nv:
            for d in diffs(ov, nv, prefix + k):
                yield d
                #~ yield "%s : %s -> %s"  % (k, ov, nv)


def compare(old, new):
    changes = list(diffs(old, new))
    if len(changes):
        msg = "Changes since %s:" % old.get('timestamp')
        msg += '\n- ' + ('\n- '.join(changes))
        #~ logger.info(msg)
        #~ logger.info('- ' + ('- '.join(changes)))
        return msg
    else:
        logger.debug("No changes since %s", old.get('timestamp'))


class Command(BaseCommand):
    help = __doc__

    def add_arguments(self, parser):
        parser.add_argument(
            '--nowrite', action='store_false',
            dest='write', default=True,
            help='Do not write status to pickle.')

    def handle(self, *args, **options):
        if args:
            raise CommandError("This command doesn't accept any arguments.")

        self.options = options

        #~ settings.SITE.startup()

        state = dict()
        state.update(timestamp=timezone.now())
        state.update(lino_version=lino.__version__)

        states_file = os.path.join(settings.SITE.project_dir, 'states.pck')

        if os.path.exists(states_file):
            fd = open(states_file)
            states_list = pickle.load(fd)
            fd.close()
            logger.info("Loaded %d states from %s",
                        len(states_list), states_file)
        else:
            states_list = []

        models_list = sorted_models_list()

        apps = [p.app_label for p in settings.SITE.installed_plugins]
        state.update(applications=" ".join(apps))
        for model in models_list:
            if model._meta.managed:
                model_state = dict()
                #~ cells.append(str(i))
                #~ cells.append(full_model_name(model))
                #~ cells.append(str(model))
                #~ if model._meta.managed:
                    #~ cells.append('X')
                #~ else:
                    #~ cells.append('')
                model_state.update(fields=[f.name for f in model._meta.fields])
                #~ qs = model.objects.all()
                qs = model.objects.order_by('pk')
                n = qs.count()
                model_state.update(rows=n)

                connection = connections[DEFAULT_DB_ALIAS]

                #~ if isinstance(connection,sqlite):
                    #~ cells.append("-")
                if mysql and isinstance(connection, mysql):

                    cursor = connection.cursor()
                    dbname = connection.settings_dict['NAME']
                    sql = """\
                    SELECT (data_length+index_length) tablesize
                    FROM information_schema.tables
                    WHERE table_schema='%s' and table_name='%s';
                    """ % (dbname, model._meta.db_table)
                    #~ print sql
                    cursor.execute(sql)
                    row = cursor.fetchone()
                    if row is not None:
                        model_state.update(bytes=row[0])
                else:
                    pass

                state[full_model_name(model)] = model_state

        if len(states_list):
            msg = compare(state, states_list[-1])
            if msg:
                logger.info(msg)
                #~ sendmail_admins()

        states_list.append(state)

        #~ print state
        if self.options['write']:
            f = open(states_file, 'w')
            pickle.dump(states_list, f)
            logger.info("Saved %d states to %s", len(states_list), states_file)
