# Copyright 2009-2014 by Luc Saffre.
# License: BSD, see LICENSE for more details.

"""

.. management_command:: initdb

Performs an initialization of the database, replacing all data by default
data (according to the specified fixtures).

This command REMOVES *all existing tables* from the database
(not only Django tables), then runs Django's `syncdb`
and `loaddata` commands to load the specified fixtures for all applications.

That may sound dangerous, but that's what you want when you ask to
restore the factory settings of a Django application.

Django's `reset` command may fail after an upgrade if the new Lino
version defines new tables. In that case, flush sends a DROP TABLE
which fails because that table doesn't exist.

This reimplements a simplified version of Django's `reset` command,
without the possibility of deleting only *some* data (the thing which
caused so big problems that Django 1.3. decided to `deprecate this command
<https://docs.djangoproject.com/en/dev/releases/1.3\
/#reset-and-sqlreset-management-commands>`__.

"""

from __future__ import unicode_literals

from optparse import make_option

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

from django.core.management.sql import sql_delete, sql_flush
from django.core.management.color import no_style
#~ from django.core.management.sql import sql_reset
from django.db import connections, transaction, DEFAULT_DB_ALIAS
from django.db import models


from lino.core.dbutils import app_labels
from lino import AFTER17
from atelier.utils import confirm

USE_SQLDELETE = True

USE_DROP_CREATE = False  # tried, but doesn't seem to work
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
        if options.get('interactive'):
            if not confirm("""We are going to flush your database (%s).
Are you sure (y/n) ?""" % dbname):
                raise CommandError("User abort.")

        options.update(interactive=False)
        #~ dblogger.info("Lino initdb %s started on database %s.", args, dbname)

        if USE_DROP_CREATE:

            from django.db import connection
            cursor = connection.cursor()
            #~ cursor.execute("DROP DATABASE %s;", [connection.settings_dict['NAME']])
            #~ cursor.execute("CREATE DATABASE %s;", [connection.settings_dict['NAME']])
            cursor.execute("DROP DATABASE %s;" % dbname)
            cursor.execute("CREATE DATABASE %s;" % dbname)

        else:

            sql_list = []
            conn = connections[using]

            if AFTER17:
                # from django.apps import apps
                # print 20140913, apps
                # app_list = apps.get_app_configs()
                sql = sql_flush(no_style(), conn, only_django=False)
                sql_list.extend(sql)

            elif USE_SQLDELETE:
                #~ sql_list = u'\n'.join(sql_reset(app, no_style(), conn)).encode('utf-8')
                app_list = [models.get_app(app_label)
                            for app_label in app_labels()]
                for app in app_list:
                    # app_label = app.__name__.split('.')[-2]
                    sql_list.extend(sql_delete(app, no_style(), conn))
                    # print app_label, ':', sql_list
            else:
                #~ call_command('flush',verbosity=0,interactive=False)
                #~ call_command('flush',**options)
                sql_list.extend(sql_flush(no_style(), conn, only_django=False))

            #~ print sql_list

            try:
                cursor = conn.cursor()
                for sql in sql_list:
                    # print sql
                    cursor.execute(sql)
            except Exception:
                transaction.rollback_unless_managed(using=using)
                raise

            transaction.commit_unless_managed()

        #~ call_command('reset',*apps,**options)
        #~ call_command('syncdb',load_initial_data=False,**options)
        #~ if USE_SQLDELETE:

        #~ tried to call `syncdb` with `verbosity=0` to avoid the
        #~ irritating message "No fixtures found" (which comes because there
        #~ are no `initial_data` fixtures):
        #~ syncdb_options = dict(**options)
        #~ syncdb_options.update(verbosity=0)
        #~ call_command('syncdb',**syncdb_options)
        #~ not good because all other messages "Creating table..." also disappear.

        #~ """
        #~ When loading a full dump back into the database,
        #~ initdb must disable the post_syncdb signal emitted by syncdb
        #~ which would cause automatisms like
        #~ `django.contrib.auth.management.create_permissions`
        #~ `django.contrib.auth.management.create_superuser`
        #~ `django.contrib.sites.management.create_default_site`
        #~ """
        #~ if options.get('dumped'):
            #~ class NullSignal:
                #~ def connect(*args,**kw):
                    #~ pass
                #~ def send(*args,**kw):
                    #~ pass
            #~ models.signals.post_syncdb = NullSignal()

        settings.SITE._site_config = None  # clear cached instance

        call_command('syncdb', load_initial_data=False, **options)

        if len(args):
            call_command('loaddata', *args, **options)

        #~ dblogger.info("Lino initdb done %s on database %s.", args, dbname)

#~ print 20120426, 'ok'
