## Copyright 2003-2005 Luc Saffre 

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

import os
from distutils.core import setup
import py2exe

from lino import __version__

dll_excludes = ['cygwin1.dll',
                'tk84.dll', 'tcl84.dll',
                '_ssl.pyd', 'pyexpat.pyd',
                '_tkinter.pyd', '_ssl.pyd'
                ]
excludes = [ "pywin", "pywin.debugger", "pywin.debugger.dbgcon",
             "pywin.dialogs", "pywin.dialogs.list",
             "Tkconstants","Tkinter","tcl",
             "wx", 'xml', 'twisted', 'mx', 'docutils'
             ]

timtools_targets = ['pds2pdf','prn2pdf','rsync', 'prnprint', 'oogen']

setup(name="timtools",
      version=__version__,
      description="Lino TIM tools",
      author="Luc Saffre",
      author_email="luc.saffre@gmx.net",
      url="http://lino.sourceforge.net/timtools.html",
      long_description="A collection of command-line tools",
      console=[ os.path.join("src","lino","scripts",t+".py")
                for t in timtools_targets],
      options= { "py2exe": { 
                   "excludes" : excludes,
                   "dll_excludes" : dll_excludes,
                 }}
      
)

del excludes['wx']

raceman_console_target = ['results']
raceman_windows_target = ['arrivals']

setup(name="raceman",
      version=__version__,
      description="Lino Raceman",
      author="Luc Saffre",
      author_email="luc.saffre@gmx.net",
      url="http://lino.sourceforge.net/raceman.html",
      long_description="""\
An uncomplete race manager.
Register participants, input arrival times,
generate results report.""",
      console=[ os.path.join("apps","raceman",t+".py")
                for t in raceman_console_target],
      windows=[ os.path.join("apps","raceman",t+".py")
                for t in raceman_windows_target],
      options= { "py2exe": { 
                   "excludes" : excludes,
                   "dll_excludes" : dll_excludes,
                 }}
      
)
