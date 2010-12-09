## Copyright 2010 Luc Saffre
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

Default logging configuration shipped with Lino.

To use it, define the following in your :xfile:`settings.py`::

  LOGGING_CONFIG = 'lino.utils.log.configure'
  LOGGING = None

See also :doc:`/tickets/closed/15`
"""

import os
import sys
import logging
from logging.handlers import RotatingFileHandler

from django.utils.log import AdminEmailHandler

def file_handler(filename):
    """
    See also :doc:`/blog/2010/1129`
    """
    if sys.platform == 'win32': 
        h = logging.FileHandler(filename)
    else:
        h = RotatingFileHandler(filename,maxBytes=100000,backupCount=5,encoding='utf-8')
    #~ if hasattr(logging,'RotatingFileHandler'):
        #~ h = logging.RotatingFileHandler(filename,maxBytes=10000,backupCount=5)
    #~ else:
        #~ h = logging.FileHandler(filename)
    fmt = logging.Formatter(
        fmt='%(asctime)s %(levelname)s %(module)s : %(message)s',
        datefmt='%Y%m-%d %H:%M:%S'
        )
    h.setFormatter(fmt)
    return h


def configure(config):
    """
    This function will be called by Django when you have your
    :setting:`LOGGING_CONFIG` set to ``'lino.utils.log.configure'``.
    """
    logger = logging.getLogger('django')
    h = AdminEmailHandler()
    h.setLevel(logging.ERROR)
    logger.addHandler(h)
    
    logger = logging.getLogger('lino')
        
    logger.setLevel(logging.DEBUG)
    
    #~ from django.conf import settings
    #~ log_dir = os.path.join(settings.PROJECT_DIR,'log')
    
    #~ if sys.stdout.isatty():
    if sys.platform == 'win32':
        h = logging.StreamHandler()
        #~ h.setLevel(logging.DEBUG)
        h.setLevel(logging.INFO)
        fmt = logging.Formatter(fmt='%(message)s')
        h.setFormatter(fmt)
        logger.addHandler(h)
    
        log_dir = 'log'
    else:
        log_dir = '/var/log/lino'
        
    if os.path.isdir(log_dir):
        h = file_handler(os.path.join(log_dir,'system.log'))
        h.setLevel(logging.DEBUG)
        logger.addHandler(h)
        
        #~ dblogger = logging.getLogger('db')
        #~ assert dblogger != logger
        #~ dblogger.setLevel(logging.INFO)
        #~ dblogger.addHandler(file_handler(os.path.join(log_dir,'db.log')))
    
    
