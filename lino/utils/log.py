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
    This provides a simplistic logging configuration for out-of-the-box usage.
    It will be called by Django when you have your
    :setting:`LOGGING_CONFIG` set to ``'lino.utils.log.configure'``.
    If you use it, then your :setting:`LOGGING` setting must be a dictionary 
    with the following keys:
    
    :param logfile:  the full path of the lino `system.log` file.
                     If absent or `None`, there will be no `system.log` file
                     
    :param level:    the verbosity level of both console and logfile messages 
                     console messages will never be more verbose than INFO
    
    Example::
    
      LOGGING_CONFIG = 'lino.utils.log.configure'
      LOGGING = dict(filename='/var/log/lino/system.log',level='INFO')
    
    Note that the `mod_wsgi documentation 
    <http://code.google.com/p/modwsgi/wiki/ApplicationIssues>`_ 
    says "code should ideally not be making assumptions about the environment it is 
    executing in, eg., whether it is running in an interactive mode, by asking whether 
    standard output is a tty. In other words, calling 'isatty()' will cause a similar error 
    with mod_wsgi. If such code is a library module, the code should be providing a way to 
    specifically flag that it is a non interactive application and not use magic to 
    determine whether that is the case or not.".
    
    """
    #~ print 20101225, config
    logfile = config.get('filename',None)
    level = getattr(logging,config.get('level','notset').upper())
    
    djangoLogger = logging.getLogger('django')
    h = AdminEmailHandler()
    h.setLevel(logging.ERROR)
    djangoLogger.addHandler(h)
    
    linoLogger = logging.getLogger('lino')
        
    linoLogger.setLevel(level)
    
    #~ from django.conf import settings
    #~ log_dir = os.path.join(settings.PROJECT_DIR,'log')
    
    try:
        if sys.stdout.isatty():
            h = logging.StreamHandler()
            #~ h.setLevel(logging.DEBUG)
            h.setLevel(logging.INFO)
            fmt = logging.Formatter(fmt='%(message)s')
            h.setFormatter(fmt)
            linoLogger.addHandler(h)
    except IOError:
        # happens under mod_wsgi
        pass
        
    if logfile is not None:
        h = file_handler(logfile)
        h.setLevel(level)
        linoLogger.addHandler(h)
        djangoLogger.addHandler(h)
        
        #~ dblogger = logging.getLogger('db')
        #~ assert dblogger != logger
        #~ dblogger.setLevel(logging.INFO)
        #~ dblogger.addHandler(file_handler(os.path.join(log_dir,'db.log')))
    
    
