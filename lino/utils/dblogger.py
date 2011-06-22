## Copyright 2010-2011 Luc Saffre
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
Since logging of database changes will inevitably cause some extra work, 
this feature is optional per site and per model.
"""

import logging
from lino import mixins
from lino.tools import obj2str

logger = logging.getLogger(__name__)

info = logger.info
warning = logger.warning
exception = logger.exception
error = logger.error
debug = logger.debug
#~ getLevel = logger.getLevel
#~ setLevel = logger.setLevel

def log_created(request,elem):
    logger.info("%s created by %s.",obj2str(elem),request.user)
    
def log_deleted(request,elem):
    logger.info("%s deleted by %s.",obj2str(elem),request.user)
    
def log_changes(request,elem):
    """logs which changes have been made to every field of `elem` 
    if `elem` is an instance of `DiffingMixin`, otherwise does nothing.
    """
    if isinstance(elem,mixins.DiffingMixin):
        changes = []
        for k,v in elem.changed_columns().items():
            changes.append("%s : %s --> %s" % (k,v['old'],v['new']))
        if len(changes) == 0:
            changes = '(no changes)'
        #~ elif len(changes) == 1:
            #~ changes = changes[0]
        else:
            changes = '\n- ' + ('\n- '.join(changes))
        msg = "%s modified by %s : %s" % (
            obj2str(elem),
            request.user,
            changes)
        #~ print msg
        logger.info(msg)

