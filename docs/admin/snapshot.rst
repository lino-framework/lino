.. _howto.snapshot:

====================================
Making a snapshot of a Lino database
====================================

.. xfile:: make_snapshot.sh

The :xfile:`make_snapshot.sh` script makes a snapshot of a Lino
database, including a Python dump (made with :manage:`dump2py`), a
`pip freeze`, configuration files, local fixtures and possibly other
local files and a `mysqldump`.

Before you can use it, your system administrator must manually copy it
from the template file :srcref:`/bash/make_snapshot.sh` to an
appropriate place on your server and adapt it to your system
environment.

When run successfully, :xfile:`make_snapshot.sh` creates a file
:file:`snapshot.zip` which contains the current state of a Lino
database. 

If a file :file:`snapshot.zip` already exists (e.g. from a previous
run), then the script renames that file by postfixing "_YYYYMMDD_hhmm"
to its base name before creating a new file.


Automated daily snapshots
=========================

:xfile:`make_snapshot.sh` behaviour of creating a backup copy is
useful when invoking the script manually at arbitrary moments. In this
situation the system adminstrator is supposed to know what they do and
to care afterwards about removing useless snapshots.

But when you run :xfile:`make_snapshot.sh` as a daily cron job, you
should take care of removing old snapshots. Otherwise your server will
run out of disk space some time in a far future when you will long
have forgotten that your daily job is adding a new file every day.

For this task we recommend to use
`logrotate <http://linuxcommand.org/man_pages/logrotate8.html>`_
because it is mature and well-known.

Sample configuration in a file :file:`/etc/logrotate.d/snapshot`::

    /var/backups/lino/mysite/snapshot.zip {
        rotate 50
        nocompress
        dateext
        dateformat _%Y%m%d
        extension .zip
        missingok
    }

You must then take care to run :xfile:`make_snapshot.sh` shortly *after*
`logrotate` because otherwise make_snapshot would rename yesterday's file before logrotate can rotate it.

For example the following :file:`/etc/crontab` specifies that
logrotate runs every morning at **6h25** (it is a script in
:file:`/etc/cron.daily`)::

    # m h dom mon dow user  command
    17 *    * * *   root    /etc/cron.hourly
    25 6    * * *   root    /etc/cron.daily )
    47 6    * * 7   root    /etc/cron.weekly )
    52 6    1 * *   root    /etc/cron.monthly )

In that case you might specify in your
:file:`/etc/cron.d/lino_backup` to run :xfile:`make_snapshot.sh` every
day at **6h33**::
    

    # Backup Lino database (Python dump) once a day
    # m h dom mon dow user  command
    33 6 * * *       www-data        /usr/local/django/mysite/make_snapshot.sh





