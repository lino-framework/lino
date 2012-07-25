#!/usr/bin/env python
import os
import sys

if True: 
    #~ don't copy this part when following the tutorial
    from os.path import dirname, join, abspath
    srcdir = abspath(join(dirname(__file__),'..'))
    if not srcdir in sys.path:
        sys.path.append(srcdir)
    #~ print sys.path
    
os.environ['DJANGO_SETTINGS_MODULE'] = 't1.settings'

import settings

from django.core.management import execute_manager

execute_manager(settings)







