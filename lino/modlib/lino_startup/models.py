# -*- coding: UTF-8 -*-
# Copyright 2013-2015 by Luc Saffre.
# License: BSD, see LICENSE for more details.

"""This module is based on Ross McFarland idea to simply send the
server startup signal "at the end of your last app's models.py file"
in his post `Django Startup Signal (Sun 24 June 2012)
<http://www.xormedia.com/django-startup-signal/>`_.

This adds a subtle hack to also cope with postponed imports.  If there
are postponed apps, then :mod:`lino.modlib.lino.models` must itself
raise an `ImportError` so that it gets itself postponed and imported
another time.

Note that `loading.cache.postponed` contains all postponed imports
even if they succeeded at the second attempt.

"""

# cannot use logging here because it causes duplicate logger setup
# in certain situations.
# import logging
# logger = logging.getLogger(__name__)

# import sys

from lino import AFTER17, site_startup

if not AFTER17:

    from django.db.models import loading

    if len(loading.cache.postponed) > 0:
        # i.e. if this is the first time
        if 'lino' not in loading.cache.postponed:
            msg = "Waiting for postponed apps (%s) to import" % \
                  loading.cache.postponed
            # logging.info("20140227 " + msg)
            raise ImportError(msg)

    site_startup()

