#coding: latin1
#---------------------------------------------------------------------
# $Id: server.py,v 1.1 2004/07/31 07:23:37 lsaffre Exp $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

"""

Copied from
http://mail.python.org/pipermail/tutor/2001-March/004157.html

"""

import os, signal, sys

def make_daemon():
	
  if os.getppid() != 1:  # we're already a daemon (started from init)
    if hasattr(signal, 'SIGTTOU'):
      signal.signal(signal.SIGTTOU, signal.SIG_IGN)
    if hasattr(signal, 'SIGTTIN'):
      signal.signal(signal.SIGTTIN, signal.SIG_IGN)
    if hasattr(signal, 'SIGTSTP'):
      signal.signal(signal.SIGTSTP, signal.SIG_IGN)
    pid = os.fork()
    if pid:
      sys.exit(0)
    os.setpgrp()
    signal.signal(signal.SIGHUP, signal.SIG_IGN)
  sys.stdin.close()
  sys.stdout.close()
  sys.stderr.close()
  os.chdir(os.sep)
  os.umask(0)
  signal.signal(signal.SIGCLD, signal.SIG_IGN)

if __name__ == '__main__':
  make_daemon()


"""

If a process tries to read from tty but was sent to background, then
the getch() will cause the process to wait until it comes back to
foreground.

asterix:/home/luc# umask
0022
asterix:/home/luc# touch tt
asterix:/home/luc# ls -ll tt
-rw-r--r--  1 root root 0 Aug 31 17:00 tt
asterix:/home/luc# umask 0
asterix:/home/luc# rm tt
asterix:/home/luc# touch tt
asterix:/home/luc# ls -ll tt
-rw-rw-rw-  1 root root 0 Aug 31 17:01 tt
asterix:/home/luc#

"""
