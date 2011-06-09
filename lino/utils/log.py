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

See also :doc:`/tickets/15`
"""

import os
import sys
import logging
from logging.handlers import RotatingFileHandler

from django.utils.log import AdminEmailHandler

def file_handler(filename,**kw):
    """
    See also :doc:`/blog/2010/1129`
    """
    kw.setdefault('encoding','UTF-8')
    if sys.platform == 'win32': 
        h = logging.FileHandler(filename,**kw)
    else:
        kw.setdefault('maxBytes',1000000)
        kw.setdefault('backupCount',10)
        h = RotatingFileHandler(filename,**kw)
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
    This provides a simplified logging configuration interface 
    for out-of-the-box usage in typical situations.
    
    It will be called by Django when you have your
    :setting:`LOGGING_CONFIG` set to ``'lino.utils.log.configure'``.
    If you use it, then your :setting:`LOGGING` setting must be a dictionary 
    with the following keys:
    
    :param logfile:  the full path of the lino `system.log` file.
                     If absent or `None`, there will be no `system.log` file.
                     
                     
    :param level:    the overall verbosity level for both console and logfile.
    
    :param mode:     the opening mode for the logfile
    :param encoding: the encoding for the logfile
    :param maxBytes: rotate if logfile's size gets bigger than this.
    :param backupCount: number of rotated logfiles to keep.
    
    Example::
    
      LOGGING_CONFIG = 'lino.utils.log.configure'
      LOGGING = dict(filename='/var/log/lino/system.log',level='INFO')
      
    If there is a logfile, then console messages will never be more verbose than INFO
    because too many messages on the screen are disturbing, 
    and if the level is DEBUG you will better analyze them in the logfile.
    
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
    encoding = config.get('encoding','UTF-8')
    logfile = config.get('filename',None)
    level = getattr(logging,config.get('level','notset').upper())
    
    djangoLogger = logging.getLogger('django')
    h = AdminEmailHandler()
    h.setLevel(logging.ERROR)
    djangoLogger.addHandler(h)
    
    linoLogger = logging.getLogger('lino')
        
    linoLogger.setLevel(level)
    
    if logfile is not None:
        kw = {}
        for k in ('mode','encoding','maxBytes','backupCount'):
            if config.has_key(k):
                kw[k] = config[k]
        h = file_handler(logfile,**kw)
        #~ h.setLevel(level)
        linoLogger.addHandler(h)
        djangoLogger.addHandler(h)
        #~ print __file__, level, logfile
        
        #~ dblogger = logging.getLogger('db')
        #~ assert dblogger != logger
        #~ dblogger.setLevel(logging.INFO)
        #~ dblogger.addHandler(file_handler(os.path.join(log_dir,'db.log')))
    
    try:
        if sys.stdout.isatty():
            #~ if sys.stdout.encoding == 'ascii':
                #~ raise Exception("Your tty's encoding is ascii, that will lead to problems" % )
            h = logging.StreamHandler()
            #~ h.setLevel(level)
            if logfile is not None:
                h.setLevel(logging.INFO)
            fmt = logging.Formatter(fmt='%(levelname)s %(message)s')
            h.setFormatter(fmt)
            linoLogger.addHandler(h)
    except IOError:
        # happens under mod_wsgi
        pass
        
