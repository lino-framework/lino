# -*- coding: UTF-8 -*-
# Copyright 2011-2012 Luc Saffre
# License: BSD (see file COPYING for details)

"""
"""

import os
import cgi
import datetime

from django.db import models
#~ from django.db.models import Q
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


from lino import mixins
from lino import dd, rt
