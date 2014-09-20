# -*- coding: UTF-8 -*-
# Copyright 2011-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Work in progress.

See :doc:`/tickets/92`.

"""

import datetime

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode

from lino import mixins
from lino import dd, rt
#~ from lino.core import reports
from lino.core import actions
from lino.utils import dblogger
from lino.core.dbutils import resolve_model
