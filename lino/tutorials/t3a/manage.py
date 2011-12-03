#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
prj = os.path.split(os.path.dirname(os.path.abspath(__file__)))[-1]
os.environ['DJANGO_SETTINGS_MODULE'] = 'lino.tutorials.' + prj + '.settings'
#~ print "DJANGO_SETTINGS_MODULE=%s" % os.environ['DJANGO_SETTINGS_MODULE']

from django.core.management import execute_manager
import settings # Required to be in the same directory.
from django.core.management import setup_environ
setup_environ(settings)

if __name__ == "__main__":
    execute_manager(settings)
