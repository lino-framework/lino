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
opj = os.path.join
import sys
import shutil
import zipfile
from time import localtime, strftime, ctime


from distutils.core import setup
import py2exe


from lino.ui.console import confirm
from lino.misc.rdir import rdirlist

from lino import __version__

VERSION = __version__

## for x in __version__.split('.'):
##     if not x.isdigit():
##         VERSION = "current"


ZIPROOT=r'u:\htdocs\timwebs\lino\dl'




args = sys.argv[1:]
sys.argv[1:] = ["py2exe"]
if len(args) == 0:
    args = ['timtools', 'raceman']

msg = "mkdist (%s) version %s" % (' '.join(args),VERSION)

if not confirm(msg):
    sys.exit(-1)


if not os.path.exists(ZIPROOT):
    raise "%s does not exist! Create it or set ZIPROOT!"

srcZipName = r'%s\lino-%s-src.zip' % (ZIPROOT,VERSION)
if os.path.exists(srcZipName):
    if not confirm("Okay to remove %s?" % srcZipName):
        distlog.write("(aborted)\n")
        raise "Pilatus problem %s" % srcZipName
    os.remove(srcZipName)
    
binZipName = r'%s\lino-%s-timtools-win32.zip' % (ZIPROOT,VERSION)
if os.path.exists(binZipName):
    if not confirm("Okay to remove %s?" % binZipName):
        distlog.write("(aborted)\n")
        raise "Pilatus problem %s" % binZipName
    os.remove(binZipName)

## if not os.path.exists(distDir):
##     os.makedirs(distDir)
## l = os.listdir(distDir)
## if len(l) > 0:
##     if confirm("Delete %d files in %s ?" % (len(l),distDir)):
##         shutil.rmtree(distDir)
##         os.makedirs(distDir)
    
    
distlog = file('dist.log','a')
distlog.write("%s started at %s...\n" % (msg, ctime()))
distlog.flush()

if confirm("write svn status to dist.log?"):
    distlog.close()
    os.system('svn stat -u >> dist.log')
    distlog = file('dist.log','a')
else:
    distlog.write("(no svn status information)\n")





DIST_ROOT = 'dist'

dll_excludes = ['cygwin1.dll',
                'tk84.dll', 'tcl84.dll',
                '_ssl.pyd', 'pyexpat.pyd',
                '_tkinter.pyd', '_ssl.pyd'
                ]
excludes = [ #"pywin", "pywin.debugger", "pywin.debugger.dbgcon",
             #"pywin.dialogs", "pywin.dialogs.list",
             "Tkconstants","Tkinter",
             "tcl",
             "wx", 'xml',
             'twisted',
             'mx',
             'docutils'
             ]


if 'timtools' in args:
    
    timtools_targets = ['pds2pdf','prn2pdf',
                        'rsync',
                        'prnprint', 'oogen']
    setup(
        name="timtools",
        version=VERSION,
        description="Lino TIM tools",
        author="Luc Saffre",
        author_email="luc.saffre@gmx.net",
        url="http://lino.sourceforge.net/timtools.html",
        long_description="A collection of command-line tools",
        dist_dir=opj(DIST_ROOT,"timtools"),
        console=[ opj("src","lino","scripts",t+".py")
                  for t in timtools_targets],
        options= { "py2exe": {
        "dist_dir" : opj(DIST_ROOT,"timtools"),
        "excludes" : excludes,
        "dll_excludes" : dll_excludes,
        }}
        
        )

if 'raceman' in args:
    
    excludes.remove('wx')

    raceman_console_target = ['results']
    raceman_windows_target = ['arrivals']

    setup(
        name="raceman",
        version=VERSION,
        description="Lino Raceman",
        author="Luc Saffre",
        author_email="luc.saffre@gmx.net",
        url="http://lino.sourceforge.net/raceman.html",
        long_description="""\
    An uncomplete race manager.
    Register participants, input arrival times,
    generate results report.""",
        console=[ opj("apps","raceman",t+".py")
                  for t in raceman_console_target],
        windows=[ opj("apps","raceman",t+".py")
                  for t in raceman_windows_target],
        options= { "py2exe": {
        "dist_dir" : opj(DIST_ROOT,"raceman"),
        "excludes" : excludes,
        "dll_excludes" : dll_excludes,
        }}
        
        )



def srcfilter(fn):
    if fn.endswith('~') : return False
    if fn.startswith('tmp') : return False
    root,ext = os.path.splitext(fn)
    if len(ext) :
        if ext.lower() in ('.pyc','.html','.zip','.pdf') :
            return False
    return True

distlog.write("done at %s\n\n" % ctime())
distlog.close()

zf = zipfile.ZipFile(srcZipName,'w',zipfile.ZIP_DEFLATED)

pruneDirs = ('.svn','_attic','CVS')

for root, dirs, files in os.walk("."):
    for pd in pruneDirs:
        try:
            dirs.remove(pd)
        except ValueError:
            pass
    for fn in files:
        if srcfilter(fn):
            zf.write(opj(srcRoot,root,fn),opj(root,fn))
            
zf.close()   

zf = zipfile.ZipFile(binZipName,'w',zipfile.ZIP_DEFLATED)
l = rdirlist(distDir)
for fn in l:
    zf.write(opj(distDir,fn),fn)
zf.write(os.path.join(srcRoot,'COPYING.txt'),'COPYING.txt')
zf.write(os.path.join(srcRoot,'dist.log'),'dist.log')
zf.close()   

