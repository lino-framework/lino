## Copyright 2010 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.

"""
:mod:`lino.utils.dblogger` -- Logging database changes
------------------------------------------------------

This module contains utilities for logging changes in a 
Django database.

It doesn't configure any logger. 
This is done either by yourself, 
or in Lino's default configuration 
:mod:`lino.demos.std.settings`
and 
:func:`lino.utils.log.configure`

    
Since logging of database changes will inevitably cause some extra work, 
this feature should be optional per site and per model.

New module :mod:`lino.utils.dblogger`
New setting :setting:`DBLOGGER`.

.. setting:: DBLOGGER

  Set this either to a logger name string or ``None``.
  Used by lino.utils.dblogger.

These two usages should have different loggers. 

On a development server, 
system logger should output `info` level messages to screen 
and `debug` messages to a file (`system.log`).
On a production server there should be no screen messages.

The database logger should log to a file `db.log`






"""

import logging
from django.conf import settings
from lino import mixins
from lino.tools import obj2str

if settings.DBLOGGER:
    logger = logging.getLogger('db')
    log = logger.info
    info = logger.info
    warning = logger.warning
    exception = logger.exception
    debug = logger.debug
    
    def log_changes(request,elem):
        if logger and isinstance(elem,mixins.DiffingMixin):
            changes = []
            for k,v in elem.changed_columns().items():
                changes.append("%s : %s --> %s" % (k,v['old'],v['new']))
            if len(changes) == 1:
                changes = changes[0]
            else:
                changes = '\n' + ('\n'.join(changes))
            msg = "%s modified by %s : %s" % (
                obj2str(elem),
                request.user,
                changes)
            logger.info(msg)

else:
    def log(*args,**kw): pass
    def info(*args,**kw): pass
    def warning(*args,**kw): pass
    def exception(*args,**kw): pass
    def debug(*args,**kw): pass
    def log_changes(request,elem): pass

