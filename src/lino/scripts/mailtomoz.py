## Copyright Luc Saffre 2003-2004.

## This file is part of the Lino project.

## Lino is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## Lino is distributed in the hope that it will be useful, but WITHOUT
## ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
## or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
## License for more details.

## You should have received a copy of the GNU General Public License
## along with Lino; if not, write to the Free Software Foundation,
## Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

"""
Wrapper to convert the `mailto` syntax (as used by browsers to call an
external mail client) to Mozilla's "-compose" command-line syntax.

Workaround for http://bugzilla.mozilla.org/show_bug.cgi?id=220306

USAGE: timtools mailtomoz MOZILLA MAILTO

Where:

  MOZILLA is the filename including path of your mozilla.exe

  MAILTO is a string of the form::

    mailto:foo@bar.com?subject=bla,body=blabla

mailtomoz will then do the following system call::

  MOZILLA -compose to=foo@bar.com,subject=bla,body=blabla

To use this script, you must edit your registry and modify the value
of `HKEY_CLASSES_ROOT\mailto\shell\open\command` to something like::

  lino mailtomoz "C:\Program files\mozilla.org\mozilla.exe" "%1"
  # or "C:\Programme\mozilla.org\Mozilla\mozilla.exe "

When bug 220306 is fixed, change this entry back to::

  C:\Programme\mozilla.org\Mozilla\mozilla.exe -mail %1

See also `openmail <openmail.html>`_.

"""

import sys,os
import urllib
from lino.ui.console import confirm

if __name__ == '__main__':

    mozilla = sys.argv[1]
    mailto = sys.argv[2]

    l = mailto.split(":",2)
    assert len(l) == 2
    assert l[0] == "mailto"
    #assert arg.startswith("mailto:")

    subject = None
    body = None
    
    l = l[1].split("?",2)
    assert len(l) >= 1
    to = urllib.unquote(l[0])
    if len(l) == 2:
        l = l[1].split('&')
        for i in l:
            name,value = i.split('=')
            if name.lower() == 'subject':
                subject = urllib.unquote(value.strip())
            elif name.lower() == 'body':
                body = urllib.unquote(value.strip())

    args = 'to=%s' % to
    if subject:
        args += ',subject=%s' % subject
    if body:
        body = body.replace('\n','\\n')
        body = body.replace('"','\\"')
        args += ',body=%s' % body
    cmd = mozilla + ' -compose "%s"' % args
    print cmd
    if not confirm("okay"): raise "not ok"
    os.system(cmd)
