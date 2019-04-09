# -*- coding: UTF-8 -*-
# Copyright 2009-2019 Rumma & Ko Ltd.
# License: BSD, see LICENSE for more details.

"""
See the page about :manage:`initdb` in the Developer's Guide.


The command performs three actions in one:

- it flushes the database specified in your :xfile:`settings.py`,
  i.e. issues a ``DROP TABLE`` for every table used by your application.

- it runs Django's :manage:`migrate` command to re-create all tables,

- it runs Django's :manage:`loaddata` command to load the specified
  fixtures.


This also adds a `warning filter
<https://docs.python.org/2/library/warnings.html#warning-filter>`__ to
ignore Django's warnings about empty fixtures. (See
:djangoticket:`18213`).

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

Note that Lino does not use Django's migration framework, so
:manage:`initdb` runs Django's `migrate` command with the
`--run-syncdb
<https://docs.djangoproject.com/en/1.11/ref/django-admin/#django-admin-option---run-syncdb>`_
option which "allows creating tables for apps without
migrations".    
The Django docs add that "While this isn’t recommended, the
migrations framework is sometimes too slow on large projects with
hundreds of models."  Yes, we go the way which is not recommended.

"""

from __future__ import unicode_literals

import os

import warnings
warnings.filterwarnings(
    "ignore", "No fixture named '.*' found.",
    UserWarning, "django.core.management.commands.loaddata")
warnings.filterwarnings(
    "ignore", "No fixture data found for *",
    RuntimeWarning, "django.core.management.commands.loaddata")

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError, OperationalError
from django.core.management.color import no_style
# ~ from django.core.management.sql import sql_reset
from django.db import connections, transaction, DEFAULT_DB_ALIAS
from django.db import models

from lino.api import dd

from lino import AFTER17, AFTER18
from atelier.utils import confirm

USE_SQLDELETE = True

USE_DROP_CREATE_DB = True
"""
http://stackoverflow.com/questions/3414247/django-drop-all-tables-from-database
http://thingsilearned.com/2009/05/10/drop-database-command-for-django-manager/

"""

def foralltables(using, cmd):
    conn = connections[using]
    cursor = conn.cursor()
    cursor.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public';")
    for tablename in cursor.fetchall():
        cursor.execute(cmd.format(tablename[0]))



class Command(BaseCommand):
    """Flush the database and load the specified fixtures.

    """

    def add_arguments(self, parser):
        parser.add_argument('fixtures', nargs='*', help='the fixtures to load')
        parser.add_argument('--noinput', action='store_false',
                            dest='interactive', default=True,
                            help='Do not prompt for input of any kind.'),
        parser.add_argument('--database', action='store', dest='database',
                            default=DEFAULT_DB_ALIAS,
                            help='Nominates a database to reset. '
                                 'Defaults to the "default" database.')

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

        using = options.get('database', DEFAULT_DB_ALIAS)
        dbname = settings.DATABASES[using]['NAME']
        engine = settings.DATABASES[using]['ENGINE']
        if options.get('interactive'):
            if not confirm("""We are going to flush your database (%s).
Are you sure (y/n) ?""" % dbname):
                raise CommandError("User abort.")
            
        fixtures = options.pop('fixtures', args)

        # print(20160817, fixtures, options)

        options.update(interactive=False)
        
        # the following log message was useful on Travis 20150104
        if options.get('verbosity', 1) > 0:
            dd.logger.info(
                "`initdb %s` started on database %s.", ' '.join(fixtures), dbname)

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
            
            # now reconnect and set foreign_key_checks to 0
            conn = connections[using]
            cursor = conn.cursor()
            cursor.execute("set foreign_key_checks=0;")
        elif engine == 'django.db.backends.postgresql':
            foralltables(using, "DROP TABLE IF EXISTS {} CASCADE;")
            # cmd = """select 'DROP TABLE "' || tablename || '" IF EXISTS CASCADE;' from pg_tables where schemaname = 'public';"""
            # cursor.execute(cmd)
            # cursor.close()
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
                from django.core.management.sql import sql_delete
                # sql_delete was removed in Django 1.9
                # ~ sql_list = u'\n'.join(sql_reset(app, no_style(), conn)).encode('utf-8')

                app_list = [models.get_app(p.app_label)
                            for p in settings.SITE.installed_plugins]
                for app in app_list:
                    # app_label = app.__name__.split('.')[-2]
                    sql_list.extend(sql_delete(app, no_style(), conn))
                    # print app_label, ':', sql_list

            # ~ print sql_list

            if len(sql_list):
                with conn.constraint_checks_disabled():
                    # for sql in sql_list:
                    #     cursor.execute(sql)

                    pending = self.try_sql(conn, sql_list)
                    while len(pending):
                        pending = self.try_sql(conn, pending)

            transaction.commit_unless_managed()

        settings.SITE._site_config = None  # clear cached instance

        if engine == 'django.db.backends.postgresql':
            # a first time to create tables of contenttypes. At
            # least on PostgreSQL this is required because for
            # some reason the syncdb fails when contenttypes is
            # not initialized.
            call_command('migrate', **options)
        call_command('migrate', '--run-syncdb', **options)

        if len(fixtures):
            # if engine == 'django.db.backends.postgresql':
            #     foralltables(using, "ALTER TABLE {} DISABLE TRIGGER ALL;")

            options.pop('interactive')
            call_command('loaddata', *fixtures, **options)
            
            # if engine == 'django.db.backends.postgresql':
            #     foralltables(using, "ALTER TABLE {} ENABLE TRIGGER ALL;")

            # dblogger.info("Lino initdb %s done on database %s.", args, dbname)
