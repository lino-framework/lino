## Copyright 2010-2013 Luc Saffre
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
Provides the default logging configuration interface 
shipped with Lino applications
for out-of-the-box usage in typical situations.
    
It defines a  function :func:`configure` which
will be called by Django when you have your
:setting:`LOGGING_CONFIG` set to ``'lino.utils.log.configure'``
(the default value set when you instantiate a :class:`lino.site.Site`)


Examples
--------

A simple common example::

  LOGGING = dict(filename='/var/log/lino/system.log',level='INFO')
  
Another example using :attr:`djangosite.Site.project_dir`::

  ...
  SITE = Site(globals()) 
  ...
  LOGGING = dict(filename=join(SITE.project_dir,'log','system.log'),level='DEBUG')

  
The following example to use date-based log files 
is **not recommended** since the filename is computed 
once per process, causing a long-running server process to log to an old file
even though a newer file has been created by another process::

  import datetime
  filename = datetime.date.today().strftime('/var/log/lino/%Y-%m-%d.log')
  LOGGING = dict(filename=filename,level='DEBUG',rotate=False)
  

Logfile rotation
----------------

On Linux systems, Lino uses WatchedFileHandler so that
system administrators can install system-wide log rotation with `logrotate`.

Django applications cannot use Python-based **Logfile rotation** 
since with Django 
it is possible to have several processes using the same :xfile:`settings.py` file.
That would sooner or later cause problems when they all try to rotate at the same time.


Remarks
-------

Yes, we read the `mod_wsgi documentation 
<http://code.google.com/p/modwsgi/wiki/ApplicationIssues>`_ 
saying "code should ideally not be making assumptions about the environment it is 
executing in, eg., whether it is running in an interactive mode, by asking whether 
standard output is a tty. In other words, calling 'isatty()' will cause a similar error 
with mod_wsgi. If such code is a library module, the code should be providing a way to 
specifically flag that it is a non interactive application and not use magic to 
determine whether that is the case or not.".
Any comments are welcome.

See also :doc:`/tickets/15`
"""

import os
import sys
import logging

#~ from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler, WatchedFileHandler
from logging.handlers import WatchedFileHandler

from django.utils.log import AdminEmailHandler

def file_handler(filename,rotate,**kw):
    #~ See also `/blog/2010/1129`
    kw.setdefault('encoding','UTF-8')
    if sys.platform == 'win32': 
        cl = logging.FileHandler
    else:
        cl = WatchedFileHandler
        #~ if kw.has_key('when'):
            #~ cl = TimedRotatingFileHandler
        #~ elif rotate:
            #~ cl = RotatingFileHandler
            #~ kw.setdefault('maxBytes',1000000)
        #~ else:
            #~ cl = WatchedFileHandler
    h = cl(filename,**kw)
    fmt = logging.Formatter(
        fmt='%(asctime)s %(levelname)s %(module)s : %(message)s',
        datefmt='%Y%m-%d %H:%M:%S'
        )
    h.setFormatter(fmt)
    return h


def configure(config):
    """
    
When using Lino's default method,
the :setting:`LOGGING` setting in your :xfile:`settings.py`
must be a dictionary containing 
the parameters you want to set. 
Available parameters are:

:param logfile:  the full path of the lino `system.log` file.
                 If absent or `None`, there will be no `system.log` file.
                 
:param level:    the overall verbosity level for both console and logfile.
:param mode:     the opening mode for the logfile
:param encoding: the encoding for the logfile
:param tty:      whether to install a default logger to the terminal

:param logger_names:  A list or tuple of names of loggers to configure.
                      If this is a string, Lino converts it to a list 
                      (expecting it to be a space-separated list of names).
                      Default value is 'djangosite north lino'.
                 
If there is a logfile, then console messages will never be more verbose than INFO
because too many messages on the screen are disturbing, 
and if the level is DEBUG you will better analyze them in the logfile.

Automatically adds an AdminEmailHandler with level ERROR to all specified loggers
*and* to the 'django' logger (even if 'django' is not specified in `loggers`).
Because that's rather necessary on a production server with :setting:`DEBUG` False.

    """
    djangoLogger = logging.getLogger('django')
    linoLogger = logging.getLogger('lino')
    #~ sudsLogger = logging.getLogger('suds')
    
    if len(linoLogger.handlers) != 0:
        msg = "Not configuring logging because lino logger already configured."
        #~ print 20130418, __file__, msg
        linoLogger.info(msg)
        return 
    
    #~ print 20101225, config
    encoding = config.get('encoding','UTF-8')
    logfile = config.get('filename',None)
    rotate = config.get('rotate',True)
    tty = config.get('tty',True)
    #~ logger_names = config.get('logger_names','djangosite north lino')
    logger_names = config.get('logger_names',None)
    #~ print 20130826, logger_names
    if not logger_names:
        #~ print 20130418, __file__, 'no logger names'
        return # Django 1.5 calls this function twice (#20229)
        #~ raise Exception("Missing keyword argument `logger_names` in %s." % config)
    #~ when = config.get('when',None)
    #~ interval = config.get('interval',None)
    level = getattr(logging,config.get('level','notset').upper())
    if isinstance(logger_names,basestring):
        logger_names = logger_names.split()
    #~ print "20130418 configure loggers", logger_names, config
    #~ if not 'lino_welfare' in logger_names:
        #~ raise Exception("20130409")
    loggers = [logging.getLogger(n) for n in logger_names]
    for l in loggers: l.setLevel(level)
    #~ linoLogger.setLevel(level)
    #~ sudsLogger.setLevel(level)
    #~ djangoLogger.setLevel(level)
    
    aeh = AdminEmailHandler(include_html=True)
    #~ aeh = AdminEmailHandler()
    aeh.setLevel(logging.ERROR)
    for l in loggers: l.addHandler(aeh)
    if not 'django' in logger_names:
        djangoLogger.addHandler(aeh)
    
    if tty:
        try:
            if sys.stdout.isatty():
                h = logging.StreamHandler()
                #~ h.setLevel(level)
                if logfile is not None:
                    h.setLevel(logging.INFO)
                #~ print "20130826 tty", h, loggers
                fmt = logging.Formatter(fmt='%(levelname)s %(message)s')
                h.setFormatter(fmt)
                for l in loggers: l.addHandler(h)
        except IOError:
            # happens under mod_wsgi
            linoLogger.info("mod_wsgi mode (no sys.stdout)")
        
    if logfile is not None:
        try:
            kw = {}
            #~ for k in ('mode','encoding','maxBytes','backupCount','when','interval'):
            for k in ('mode','encoding'):
                if config.has_key(k):
                    kw[k] = config[k]
            h = file_handler(logfile,rotate,**kw)
            #~ h.setLevel(level)
            for l in loggers: l.addHandler(h)
            #~ linoLogger.addHandler(h)
            #~ djangoLogger.addHandler(h)
            #~ sudsLogger.addHandler(h)
            #~ print __file__, level, logfile
            
            #~ dblogger = logging.getLogger('db')
            #~ assert dblogger != logger
            #~ dblogger.setLevel(logging.INFO)
            #~ dblogger.addHandler(file_handler(os.path.join(log_dir,'db.log')))
        except IOError,e:
            #~ linoLogger.exception("Failed to create log file %s : %s",logfile,e)
            linoLogger.exception(e)
            
    
    #~ linoLogger.info("20120408 linoLogger.handlers: %s", linoLogger.handlers)

