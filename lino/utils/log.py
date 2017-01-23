# Copyright 2010-2017 Luc Saffre
# License: BSD (see file COPYING for details)

"""
**No longer used since :blogref:`20160712`.**

Provides the default logging configuration interface shipped with
Lino applications for out-of-the-box usage in typical situations.
    
It defines a function :func:`configure` which will be called by Django
when you have your :setting:`LOGGING_CONFIG` set to
``'lino.utils.log.configure'`` (the default value set when you
instantiate a :class:`lino.core.site.Site`)

In order to disable Lino's system, you can either set
:setting:`LOGGING_CONFIG` to your own value, you configure logging
yourself manually *before* Lino starts. For example by writing at the
begnning of your :xfile:`manage.py` file::

    import logging
    logging.basicConfig(level=logging.INFO)

Or when you want to log things that happen *before* Django calls
:func:`lino.utils.log.configure`, then you must also manually
configure logging.

Examples
--------

A simple common example::

  LOGGING = dict(filename='/var/log/lino/system.log',level='INFO')

Another example using :attr:`lino.core.site.Site.project_dir`::

  ...
  SITE = Site(globals())
  ...
  LOGGING = dict(
      filename=join(SITE.project_dir, 'log', 'system.log'),
      level='DEBUG')


The following example to use date-based log files is **not
recommended** since the filename is computed once per process, causing
a long-running server process to log to an old file even though a
newer file might have been created by another process::

  import datetime
  filename = datetime.date.today().strftime('/var/log/lino/%Y-%m-%d.log')
  LOGGING = dict(filename=filename,level='DEBUG',rotate=False)


Logfile rotation
----------------

Django applications cannot use Python-based **Logfile rotation** since
with Django it is possible to have several processes using the same
:xfile:`settings.py` file.  That would sooner or later cause problems
when they all try to rotate at the same time.

On Linux systems, Lino uses WatchedFileHandler so that system
administrators can install system-wide log rotation with `logrotate`.


Remarks
-------

Yes, we read the `mod_wsgi documentation
<http://code.google.com/p/modwsgi/wiki/ApplicationIssues>`_ saying
"code should ideally not be making assumptions about the environment
it is executing in, eg., whether it is running in an interactive mode,
by asking whether standard output is a tty. In other words, calling
'isatty()' will cause a similar error with mod_wsgi. If such code is a
library module, the code should be providing a way to specifically
flag that it is a non interactive application and not use magic to
determine whether that is the case or not.".  Any comments are
welcome.

See also :srcref:`docs/tickets/15`

"""
from __future__ import print_function
import six

import os
import sys
import logging

from logging.handlers import WatchedFileHandler


def file_handler(filename, rotate, **kw):
    #~ See also `/blog/2010/1129`
    kw.setdefault('encoding', 'UTF-8')
    if sys.platform == 'win32':
        cl = logging.FileHandler
    else:
        cl = WatchedFileHandler
    h = cl(filename, **kw)
    fmt = logging.Formatter(
        fmt='%(asctime)s %(levelname)s %(module)s : %(message)s',
        datefmt='%Y%m-%d %H:%M:%S'
    )
    h.setFormatter(fmt)
    return h


def configure(config):
    """When using Lino's default method, the :setting:`LOGGING` setting in
your :xfile:`settings.py` must be a dictionary containing the
parameters you want to set.  Available parameters are:

:param logfile:  the full path of the lino `system.log` file.
                 If absent or `None`, there will be no `system.log` file.
                 
:param level:    the overall verbosity level for both console and logfile.
:param mode:     the opening mode for the logfile
:param encoding: the encoding for the logfile
:param tty:      whether to install a default logger to the terminal

:param logger_names:  A list or tuple of names of loggers to configure.
                      If this is a string, Lino converts it to a list 
                      (expecting it to be a space-separated list of names).
                      Default value is 'lino'.
                 
If there is a logfile, then console messages will never be more
verbose than INFO because too many messages on the screen are
disturbing, and if the level is DEBUG you will better analyze them in
the logfile.

Automatically adds an AdminEmailHandler with level ERROR to all
specified loggers *and* to the 'django' logger (even if 'django' is
not specified in `loggers`).  Because that's rather necessary on a
production server with :setting:`DEBUG` False.

    """
    from django.apps import apps
    # from django.conf import settings
    msg = "20160711 %s / %s" % (config, apps.apps_ready)
    
    # msg = "20160711 %s / %s" % (config, logging._handlerList)
    # raise Exception(msg)
    print(msg)

    if not apps.models_ready:
        msg = "Not changing the existing logging configuration."
        # raise Exception(msg)
        logging.info(msg)
        return

    # if getattr(logging, "set_up_done", False):
    #     msg = "Not changing the existing logging configuration."
    #     # raise Exception(msg)
    #     logging.info(msg)
    #     return
    # logging.set_up_done = True

    # if configure.has_been_called:
    #     msg = "Not changing the existing logging configuration."
    #     # raise Exception(msg)
    #     logging.info(msg)
    #     return
    # configure.has_been_called = True

    # if len(logging.root.handlers) != 0:
    # if len(logging._handlerList) != 0:
    #     msg = "Not changing the existing logging configuration."
    #     # raise Exception(msg)
    #     logging.info(msg)
    #     return

    #~ logger_names = config.get('logger_names','djangosite lino')
    logger_names = config.get('logger_names', None)
    #~ print 20130826, logger_names
    if not logger_names:
        #~ print 20130418, __file__, 'no logger names'
        return  # Django 1.5 calls this function twice (#20229)
        #~ raise Exception("Missing keyword argument `logger_names` in %s." % config)

    djangoLogger = logging.getLogger('django')
    linoLogger = logging.getLogger('lino')

    from django.utils.log import AdminEmailHandler

    # print 20150623, config
    # encoding = config.get('encoding', 'UTF-8')
    logfile = config.get('filename', None)
    rotate = config.get('rotate', True)
    tty = config.get('tty', True)

    level = getattr(logging, config.get('level', 'notset').upper())
    if isinstance(logger_names, six.string_types):
        logger_names = logger_names.split()
    # print "20130418 configure loggers", logger_names, config
    loggers = [logging.getLogger(n) for n in logger_names]

    # for l in loggers:
    #     if len(l.handlers) != 0:
    #         msg = "Not configuring logging because already configured."
    #         l.info(msg)
    #         return

    for l in loggers:
        l.setLevel(level)

    aeh = AdminEmailHandler(include_html=True)
    aeh.setLevel(logging.ERROR)
    for l in loggers:
        l.addHandler(aeh)
    if 'django' not in logger_names:
        djangoLogger.addHandler(aeh)

    if tty:
        try:
            if sys.stdout.isatty():
                h = logging.StreamHandler()
                if logfile is not None:
                    h.setLevel(logging.INFO)
                #~ print "20130826 tty", h, loggers
                fmt = logging.Formatter(fmt='%(levelname)s %(message)s')
                h.setFormatter(fmt)
                for l in loggers:
                    l.addHandler(h)
        except IOError:
            # happens under mod_wsgi
            linoLogger.info("mod_wsgi mode (no sys.stdout)")

    if logfile is not None:
        try:
            kw = {}
            for k in ('mode', 'encoding'):
                if k in config:
                    kw[k] = config[k]
            h = file_handler(logfile, rotate, **kw)
            #~ h.setLevel(level)
            for l in loggers:
                l.addHandler(h)

        except IOError as e:
            raise Exception("Failed to create log file %s : %s" % (logfile, e))
            # linoLogger.exception("Failed to create log file %s : %s", logfile, e)
            # linoLogger.exception(e)


    #~ linoLogger.info("20120408 linoLogger.handlers: %s", linoLogger.handlers)


# configure.has_been_called = False
