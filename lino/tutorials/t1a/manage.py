#!/usr/bin/env python
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'lino.tutorials.t1a.settings'

import settings

from django.core.management import execute_manager

execute_manager(settings)







