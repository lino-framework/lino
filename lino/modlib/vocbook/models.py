# -*- coding: UTF-8 -*-
# Copyright 2011-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Database models for `lino.modlib.vocbook`.

.. autosummary::

Work in progress.

See :srcref:`docs/tickets/92`.

"""

import datetime

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_text

from lino import mixins
from lino.api import dd, rt
#~ from lino.core import reports
from lino.core import actions
from lino.utils import dblogger
from lino.core.utils import resolve_model
