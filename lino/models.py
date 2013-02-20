# -*- coding: UTF-8 -*-
## Copyright 2013 Luc Saffre
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
This module is Lino's implementation of 
Ross McFarland idea to simply send the server startup signal
"at the end of your last app's models.py file"
in his post `Django Startup Signal (Sun 24 June 2012)
<http://www.xormedia.com/django-startup-signal/>`_.

Lino adds a subtle hack to also cope with postponed imports.
If there are postponed apps, then :mod:`lino.models` must itself raise 
an `ImportError` so that it gets itself postponed and imported another 
time.

Note that `loading.cache.postponed` 
contains all postponed imports even if they succeeded 
at the second attempt.
"""

import sys
from django.db.models import loading

if len(loading.cache.postponed) > 0:
    if not 'lino' in loading.cache.postponed: # i.e. if this is the first time
        raise ImportError("Waiting for postponed apps (%s) to import" % 
            loading.cache.postponed)


from django.conf import settings
settings.LINO.startup()
