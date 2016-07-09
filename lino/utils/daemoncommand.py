"""Copyright (c) 2009, Sean Creeley
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

  * Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.

  * Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in
    the documentation and/or other materials provided with the
    distribution.

  * Neither the name of the Optaros, Inc. nor the names of its
    contributors may be used to endorse or promote products derived
    from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT
OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Modifications by Luc Saffre :

- fixed: Overriding default values in a subclass didn't work.
  `/blog/2010/1210`
  
- added `DaemonCommand.preserve_loggers` class variable and
  :func:`get_handlers` and :func:`get_logger_files`.
  `/blog/2010/1214`
  
- when a pidfile is specified and a file of that name already exists,
  DaemonCommand now no longer waits forever but raises a LockTimeout
  See `/blog/2011/0126` and
  http://packages.python.org/lockfile/lockfile.html#lockfile.FileLock.acquire.
  
- now works with versions of `daemon` who use "pidfile" instead of
  "pidlockfile".
  
- 20130610 Changes needed for Django 1.5: No longer overrides `handle`
  but `execute`.  Converts any options 'stdout' and 'stderr' if given
  because Django expects them to be file-like objects (not names of
  files).  Removed the stderr, stdout and stdin class attributes
  because they interferred with Django.

- :blogref:`20160607` converted from optparse to argparse (changes
  needed for Django 1.10)


=============
DaemonCommand
=============

Django Management Command for starting a daemon.

Use
===

Simple use of daemon command::

    from daemonextension import DaemonCommand
    from django.conf import settings
    import os
    
    class Command(DaemonCommand):
        
        stdout = os.path.join(settings.DIRNAME, "log/cubbyscott.out")
        stderr = os.path.join(settings.DIRNAME, "log/cubbyscott.err")
        pidfile = os.path.join(settings.DIRNAME, "pid/cb_link.pid")
        
        def handle_daemon(self, *args, **options):
            from flopsy import Connection, Consumer
            consumer = Consumer(connection=Connection())
            consumer.declare(queue='links',
                             exchange='cubbyscott',
                             routing_key='importer', auto_delete=False)
            
            def message_callback(message):
                print 'Recieved: ' + message.body
                consumer.channel.basic_ack(message.delivery_tag)
            
            consumer.register(message_callback)
            
            consumer.wait()

call::

    python python manage.py linkconsumer

"""

import logging
from django.core.management.base import BaseCommand


def get_handlers(logger):
    while logger:
        for h in logger.handlers:
            yield h
        if not logger.propagate:
            logger = None  # break out
        else:
            logger = logger.parent


def get_logger_files(loggers):
    """Return a list of the file handles used by the specified loggers.
    Thanks to
    http://mail.python.org/pipermail/python-list/2010-April/1241406.html

    """
    l = []
    for logger in loggers:
        for h in get_handlers(logger):
            if isinstance(h, logging.StreamHandler):
                l.append(h.stream.fileno())
    return l

try:
    import daemon  # pip install python-daemon
    # in older versions it's called pidlockfile, later just pidfile
    try:
        from daemon import pidlockfile
    except ImportError:
        from daemon import pidfile as pidlockfile

except ImportError:

    daemon = None

    """On systems that don't support daemons, we just emulate.
  """


class DaemonCommand(BaseCommand):

    """If you have an existing Django management command, just rename
    it's `handle` method to `handle_daemon` and inherit from this
    instead of :class:`django.core.management.base.BaseCommand`.

    """

    help = 'Create a daemon'

    # chroot_directory = None
    # working_directory = '/'
    # umask = 0
    # detach_process = True
    # prevent_core = True
    # # stdin = None
    # # stdout = None
    # # stderr = None
    # pidfile = None
    # uid = None
    # gid = None

    """The loggers to preserve. If not None, this should be a list of
    loggers (:class:`logging.Logger` instances) whose file handles
    should not get closed.

    """
    preserve_loggers = None

    def add_arguments(self, parser):
        super(DaemonCommand, self).add_arguments(parser)
        parser.add_argument(
            '--chroot_directory', action='store',
            dest='chroot_directory',
            help="Full path to a directory to set as the "
            "effective root directory of the process.")
        parser.add_argument(
            '--working_directory', action='store',
            dest='working_directory',
            default="/",
            help="Full path of the working directory to which the "
            "process should change on daemon start.")
        parser.add_argument(
            '--umask', action='store', dest='umask',
            default=0, type=int,
            help='File access creation mask ("umask") to set for '
            'the process on daemon start.')
        parser.add_argument(
            '--pidfile', action='store', dest='pidfile',
            help='Context manager for a PID lock file. When the '
            'daemon context opens and closes, it enters and exits '
            'the `pidfile` context manager.')
        parser.add_argument(
            '--detach_process', action='store', dest='detach_process',
            help='If ``True``, detach the process context when opening '
            'the daemon context; if ``False``, do not detach.')
        parser.add_argument(
            '--uid', action='store', dest='uid',
            help='The user ID ("UID") value to switch the process to '
            'on daemon start.')
        parser.add_argument(
            '--gid', action='store', dest='gid',
            help='The group ID ("GID") value to switch the process to '
            'on daemon start.')
        parser.add_argument(
            '--prevent_core', action='store', dest='prevent_core',
            default=True,
            help='If true, prevents the generation of core files, '
            'in order to avoid leaking sensitive information from '
            'daemons run as `root`.')
        parser.add_argument(
            '--stdin', action='store', dest='stdin',
            help='Standard In')
        parser.add_argument(
            '--stdout', action='store', dest='stdout',
            help='Standard Out'),
        parser.add_argument(
            '--stderr', action='store', dest='stderr',
            help='Standard Error')

    # def create_parser(self, *args, **kw):
    #     p = super(DaemonCommand, self).create_parser(*args, **kw)
    #     p.set_defaults(
    #         chroot_directory=self.chroot_directory,
    #         working_directory=self.working_directory,
    #         umask=self.umask,
    #         detach_process=self.detach_process,
    #         prevent_core=self.prevent_core,
    #         # stdin = self.stdin,
    #         # stdout = self.stdout,
    #         # stderr = self.stderr,
    #         pidfile=self.pidfile,
    #         uid=self.uid,
    #         gid=self.gid)
    #     return p

    def get_option_value(self, options, name, expected=None):
        return options.get(name)  # ,getattr(self,name))

    def execute(self, *args, **options):
        """
        Takes the options and starts a daemon context from them.

        Example::

            python manage.py linkconsumer --pidfile=/var/run/cb_link.pid
                --stdout=/var/log/cb/links.out --stderr=/var/log/cb/links.err

        """
        # print 20130610, 'execute', __file__

        # print options

        if daemon is not None:

            context = daemon.DaemonContext()

            context.chroot_directory = self.get_option_value(
                options, 'chroot_directory')
            context.working_directory = self.get_option_value(
                options, 'working_directory', '/')
            context.umask = self.get_option_value(options, 'umask', 0)
            context.detach_process = self.get_option_value(
                options, 'detach_process')
            context.prevent_core = self.get_option_value(
                options, 'prevent_core', True)
            if self.preserve_loggers:
                context.files_preserve = get_logger_files(
                    self.preserve_loggers)

            # Get file objects
            # stdin =  self.get_option_value(options, 'stdin')
            stdin = options.pop('stdin', None)
            if stdin is not None:
                options['stdin'] = context.stdin = open(stdin, "r")

            # stdout = self.get_option_value(options, 'stdout')
            stdout = options.pop('stdout', None)
            if stdout is not None:
                options['stdout'] = context.stdout = open(stdout, "a+")

            # stderr = self.get_option_value(options, 'stderr')
            stderr = options.pop('stderr', None)
            if stderr is not None:
                self.stderr = options[
                    'stderr'] = context.stderr = open(stderr, "a+")
            # self.stderr is needed in case there is an exception
            # during execute.  Django then would try to write to
            # sys.stderr which is None because we are a daemon

            # Make pid lock file
            pidfile = self.get_option_value(options, 'pidfile')
            if pidfile is not None:
                # context.pidfile=pidlockfile.PIDLockFile(pidfile)
                context.pidfile = pidlockfile.TimeoutPIDLockFile(pidfile, 0)

            uid = self.get_option_value(options, 'uid')
            if uid is not None:
                context.uid = int(uid)

            gid = self.get_option_value(options, 'gid')
            if gid is not None:
                context.gid = int(gid)

            context.open()

        # Django 1.5.1 needs them:
        # for k in ('stdout','stderr'):
        #     options[k] = getattr(context,k,None)

        # self.handle_daemon(*args, **options)
        BaseCommand.execute(self, *args, **options)
        # print 20130610, 'execute ok', __file__
