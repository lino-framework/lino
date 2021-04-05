# Copyright 2010-2011 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""
Just a shortcut and encapsulation. Instead of writing::

    import logging
    logger = logging.getLogger(__name__)
    
I (sometimes) prefer to write::

    from lino.utils import dblogger

"""

import logging
logger = logging.getLogger(__name__)
info = logger.info
warning = logger.warning
exception = logger.exception
error = logger.error
debug = logger.debug
#~ getLevel = logger.getLevel
#~ setLevel = logger.setLevel

from lino.core.utils import obj2str


def log_deleted(request, elem):
    #~ on_user_change(request,elem)
    logger.info(u"%s deleted by %s.", obj2str(elem), request.user)
