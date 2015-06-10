# Copyright 2009-2015 by Luc Saffre.
# License: BSD, see LICENSE for more details.

""".. management_command:: initdb

Performs an initialization of the database, replacing all data by default
data (according to the specified fixtures).

This command REMOVES *all existing tables* from the database (not only
Django tables), then runs Django's `syncdb` (or `migrate`) to create
all tables, and `loaddata` commands to load the specified fixtures for
all applications.

This reimplements a simplified version of Django's `reset` command,
without the possibility of deleting *only some* data (the thing which
caused so big problems that Django 1.3. decided to `deprecate this
command <https://docs.djangoproject.com/en/dev/releases/1.3\
/#reset-and-sqlreset-management-commands>`__.

Deleting all data and table definitions from a database is not always
trivial. It is not tested on PostgreSQL. In MySQL we use a somewhat
hackerish and MySQL-specific DROP DATABASE and CREATE DATABASE because
even with `constraint_checks_disabled` we had sporadic errors. See
:blogref:`20150328`

"""

from __future__ import unicode_literals

import os
from optparse import make_option

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError, OperationalError
from django.core.management.sql import sql_delete, sql_flush
from django.core.management.color import no_style
#~ from django.core.management.sql import sql_reset
from django.db import connections, transaction, DEFAULT_DB_ALIAS
from django.db import models


from lino.api import dd

from lino.core.utils import app_labels
from lino import AFTER17
from atelier.utils import confirm

USE_SQLDELETE = True

USE_DROP_CREATE_DB = True
"""
http://stackoverflow.com/questions/3414247/django-drop-all-tables-from-database
http://thingsilearned.com/2009/05/10/drop-database-command-for-django-manager/

"""


class Command(BaseCommand):
    help = __doc__

    args = "fixture [fixture ...]"

    option_list = BaseCommand.option_list + (
        make_option(
            '--noinput', action='store_false',
            dest='interactive', default=True,
            help='Do not prompt for input of any kind.'),
        make_option(
            '--database', action='store', dest='database',
            default=DEFAULT_DB_ALIAS,
            help='Nominates a database to reset. '
            'Defaults to the "default" database.'),
    )

    def try_sql(self, conn, sql_list):
        hope = False
        pending = []
        errors = []
        cursor = conn.cursor()
        for sql in sql_list:
            try:
                cursor.execute(sql)
                hope = True
            except (IntegrityError, OperationalError) as e:
                pending.append(sql)
                errors.append(e)
        if not hope:
            # a temporary last attempt: run them all in one statement
            # sql = "SET foreign_key_checks=0;" + ';'.join(sql_list)
            # cursor.execute(sql)

            msg = "%d pending SQL statements failed:" % len(pending)
            for i, sql in enumerate(pending):
                e = errors[i]
                msg += "\n%s :\n  %s\n  %s" % (e.__class__, sql, e)
            raise Exception(msg)
        return pending

    def handle(self, *args, **options):

        #~ from lino.core.kernel import analyze_models
        #~ analyze_models()

        #~ from lino.utils import dblogger

        #~ if not dblogger.logger.isEnabledFor(logging.INFO):
            #~ raise CommandError("System logger must be enabled for INFO")
        #~ dblogger.info(settings.SITE.welcome_text())
        #~ dblogger.info("FIXTURE_DIRS is %s",settings.FIXTURE_DIRS)
        using = options.get('database', DEFAULT_DB_ALIAS)
        dbname = settings.DATABASES[using]['NAME']
        engine = settings.DATABASES[using]['ENGINE']
        if options.get('interactive'):
            if not confirm("""We are going to flush your database (%s).
Are you sure (y/n) ?""" % dbname):
                raise CommandError("User abort.")

        options.update(interactive=False)
        # the following log message was useful on Travis 20150104
        dd.logger.info(
            "`initdb %s` started on database %s.", ' '.join(args), dbname)

        if engine == 'django.db.backends.sqlite3':
            if dbname != ':memory:' and os.path.isfile(dbname):
                os.remove(dbname)
                del connections[using]
        elif engine == 'django.db.backends.mysql':
            conn = connections[using]
            cursor = conn.cursor()
            cursor.execute("DROP DATABASE %s;" % dbname)
            cursor.execute("CREATE DATABASE %s charset 'utf8';" % dbname)
            # We must now force Django to reconnect, otherwise we get
            # "no database selected" since Django would try to
            # continue on the dropped database:
            del connections[using]
        else:
            raise Exception("Not tested for %r" % engine)
            sql_list = []
            conn = connections[using]

            # adds a "DELETE FROM tablename;" for each table
            # sql = sql_flush(no_style(), conn, only_django=False)
            # sql_list.extend(sql)

            if AFTER17:
                # django.core.management.base.CommandError: App
                # 'sessions' has migrations. Only the sqlmigrate and
                # sqlflush commands can be used when an app has
                # migrations.
                # from django.apps import apps
                # app_list = apps.get_app_configs()
                # for app in app_list:
                #     sql_list.extend(sql_delete(app, no_style(), conn))
                pass

            elif USE_SQLDELETE:
                #~ sql_list = u'\n'.join(sql_reset(app, no_style(), conn)).encode('utf-8')
                
                app_list = [models.get_app(app_label)
                            for app_label in app_labels()]
                for app in app_list:
                    # app_label = app.__name__.split('.')[-2]
                    sql_list.extend(sql_delete(app, no_style(), conn))
                    # print app_label, ':', sql_list

            #~ print sql_list

            if len(sql_list):
                with conn.constraint_checks_disabled():
                    # for sql in sql_list:
                    #     cursor.execute(sql)

                    pending = self.try_sql(conn, sql_list)
                    while len(pending):
                        pending = self.try_sql(conn, pending)

                # conn.disable_constraint_checking()
                # try:
                #     cursor = conn.cursor()
                #     pending = self.try_sql(cursor, sql_list)
                #     while len(pending):
                #         pending = self.try_sql(cursor, pending)

                # except Exception:
                #     transaction.rollback_unless_managed(using=using)
                #     raise
                # conn.enable_constraint_checking()

            transaction.commit_unless_managed()

        settings.SITE._site_config = None  # clear cached instance

        if AFTER17:
            call_command('migrate', **options)
        else:
            call_command('syncdb', load_initial_data=False, **options)

        if len(args):
            call_command('loaddata', *args, **options)

        #~ dblogger.info("Lino initdb done %s on database %s.", args, dbname)

#~ print 20120426, 'ok'
