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

If looks for a logger named ``'db'``. 
If such a logger didn't yet exist, we do a default configuration.

    
Since logging of database changes will inevitably cause some extra work, 
this feature should be optional per site and per model.

New setting :setting:`DBLOGFILE`.

.. setting:: DBLOGFILE

  The full path of the changelog file.
  If this is ``None``, database changelogs are disabled.
  If this is ``'auto'``, the file will be named 
  :xfile:`db.log` in a :file:`log` subdir of your :setting:`PROJECT_DIR`.

  Default value ``'auto'`` is defined in 
  :mod:`lino.demos.std.settings`.






"""

from django.conf import settings

if settings.DBLOGFILE:
  
    import os
    import logging
    from logging.handlers import RotatingFileHandler
    from lino import mixins
    from lino.tools import obj2str
    from lino.utils.log import file_handler
    
    logger = logging.getLogger('db')
    #~ log = logger.info
    info = logger.info
    warning = logger.warning
    exception = logger.exception
    error = logger.error
    debug = logger.debug
    
    if len(logger.handlers) == 0:
        filename = settings.DBLOGFILE
        if filename.lower() == 'auto':
            filename = os.path.join(settings.PROJECT_DIR,'log','db.log')
        logger.setLevel(logging.INFO)
        logger.addHandler(file_handler(filename))
      
    
    def log_changes(request,elem):
        if isinstance(elem,mixins.DiffingMixin):
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
    #~ def log(*args,**kw): pass
    def info(*args,**kw): pass
    def warning(*args,**kw): pass
    def exception(*args,**kw): pass
    def error(*args,**kw): pass
    def debug(*args,**kw): pass
    def log_changes(request,elem): pass

