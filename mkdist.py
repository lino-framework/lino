## Copyright 2003-2007 Luc Saffre 

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


from lino.console import syscon
from lino.misc.rdir import rdirlist

from lino import __version__, __url__

#VERSION = __version__
DIST_ROOT = 'dist'
#DLROOT=r'u:\htdocs\timwebs\lino\dl'


class InnoScript:
    """inspired by py2exe/samples/extending/setup.py
    
    My version just takes all the files in the directory.  You must
    just specify names of the Windows executables without any
    directory name. All files that are not in this list will be
    considered library files. Sub-directories are not supported.
    
    """
    def __init__(self, name, dist_dir, version,
                 windows_exe_files = []
                 ):
        self.dist_dir = dist_dir
        if not self.dist_dir[-1] in "\\/":
            self.dist_dir += "\\"
        self.name = name
        self.version = version
        self.windows_exe_files = windows_exe_files
        self.lib_files = []
        for fn in os.listdir(self.dist_dir):
            if fn == "Output":
                pass
            elif not fn in self.windows_exe_files:
                self.lib_files.append(fn)
                
    def create(self, pathname=None):
        if pathname is None:
            pathname = self.dist_dir+"\\"+self.name+".iss"
        self.pathname = pathname
        ofi = self.file = open(pathname, "w")
        print >> ofi, "; WARNING: This script has been created by py2exe. Changes to this script"
        print >> ofi, "; will be overwritten the next time py2exe is run!"
        print >> ofi, r"[Setup]"
        print >> ofi, r"AppName=%s" % self.name
        print >> ofi, r"AppVerName=%s %s" % (self.name, self.version)
        print >> ofi, r"DefaultDirName={pf}\%s" % self.name
        print >> ofi, r"DefaultGroupName=%s" % self.name
        print >> ofi, r"OutputBaseFilename=%s-%s-setup" % (
            self.name, self.version)
        print >> ofi, r"OutputManifestFile=%s-%s-manifest.txt" % (
            self.name, self.version)
        
        print >> ofi

        print >> ofi, r"[Files]"
        for path in self.windows_exe_files + self.lib_files:
            print >> ofi, r'Source: "%s"; DestDir: "{app}\%s"; Flags: ignoreversion' % (path, os.path.dirname(path))
        print >> ofi

        print >> ofi, r"[Icons]"
        for path in self.windows_exe_files:
            print >> ofi, r'Name: "{group}\%s"; Filename: "{app}\%s"' % \
                  (self.name, path)
        print >> ofi, 'Name: "{group}\Uninstall %s"; Filename: "{uninstallexe}"' % self.name
        ofi.close()

    def compile(self):
        try:
            import ctypes
        except ImportError:
            try:
                import win32api
            except ImportError:
                import os
                os.startfile(self.pathname)
            else:
                print "Ok, using win32api."
                win32api.ShellExecute(0, "compile",
                                      self.pathname,
                                      None,
                                      None,
                                      0)
        else:
            print "Cool, you have ctypes installed."
            res = ctypes.windll.shell32.ShellExecuteA(0, "compile",
                                                      self.pathname,
                                                      None,
                                                      None,
                                                      0)
            if res < 32:
                raise RuntimeError, "ShellExecute failed, error %d" % res




## if not os.path.exists(DLROOT):
##     raise "%s does not exist! Create it or set DLROOT!"



args = sys.argv[1:]
# sys.args will be rewritten later
if len(args) == 0:
    args = ['timtools', 'raceman', 'keeper', 'sdist']

msg = "mkdist (%s) version %s" % (' '.join(args),__version__)
print msg

## if not syscon.confirm(msg):
##     sys.exit(-1)
 
## distlog = file('dist.log','a')
## distlog.write("%s started at %s...\n" % (msg, ctime()))
## distlog.flush()

## if console.confirm("write svn status to dist.log?"):
##     distlog.close()
##     os.system('svn stat -u >> dist.log')
##     distlog = file('dist.log','a')
## else:
##     distlog.write("(no svn status information)\n")





dll_excludes = ['cygwin1.dll',
                'tk84.dll', 'tcl84.dll',
                '_ssl.pyd', 'pyexpat.pyd',
                '_tkinter.pyd', '_ssl.pyd',
                'QtGui4.dll',
                'QtCore4.dll', 'QtCore4.pyd',
                'QtSql4.dll', 'QtSql.pyd', 
                'MSVCR71.dll',
                'mingwm10.dll',
                ]
excludes = [ #"pywin", "pywin.debugger", "pywin.debugger.dbgcon",
             #"pywin.dialogs", "pywin.dialogs.list",
             #'xml',
             "Tkconstants","Tkinter",
             "tcl",
             'twisted',
             'mx',
             'docutils'
             ]

excludes_console = excludes + ['wx']


if 'timtools' in args:
    
    from lino import timtools
    
    sys.argv[1:] = ["py2exe"]
    
    console_targets = timtools.CONSOLE_TARGETS

    name = "timtools"

    dist_dir = opj(DIST_ROOT,name)
    
    setup(
        name=name,
        version=__version__,
        description="Lino TIM tools",
        author="Luc Saffre",
        author_email="luc.saffre@gmx.net",
        url=__url__+"/timtools.html",
        long_description="A collection of command-line tools to help DOS applications survive",
        package_dir = {'': 'src'},
        console=[ opj("src","lino","scripts",t+".py")
                  for t in console_targets],
        options= { "py2exe": {
        "compressed": 1,
        "optimize": 2,
        "dist_dir" : dist_dir,
        "excludes" : excludes_console,
        "includes": ["encodings.*",
                     "email.iterators",
                     "email.generator",
                     #"encodings.cp850",
                     #"encodings.cp1252",
                     #"encodings.iso-8859-1"
                     ],
        "dll_excludes" : dll_excludes,
        }}
        
        )

    zipname = "%s-%s-py2exe.zip" % (name,__version__)
    zipname = opj(DIST_ROOT,zipname)
    zf = zipfile.ZipFile(zipname,'w',zipfile.ZIP_DEFLATED)
    l = rdirlist(dist_dir)
    for fn in l:
        zf.write(opj(dist_dir,fn),opj(name,fn))
    for fn in ['COPYING.txt']:
        zf.write(fn,opj(name,fn))
    zf.close()   

if 'hello' in args:
    
    sys.argv[1:] = ["py2exe"]
    
    console_targets = ["hello"]

    name = "hello"

    dist_dir = opj(DIST_ROOT,name)
    
    setup(
        name=name,
        version=__version__,
        description="Lino Hello",
        author="Luc Saffre",
        author_email="luc.saffre@gmx.net",
        url=__url__+"/hello.html",
        long_description='"Hello, world!"',
        package_dir = {'': 'src'},
        console=[ opj("src","lino","scripts","hello.py")],
        options= { "py2exe": {
        "compressed": 1,
        "optimize": 2,
        "dist_dir" : dist_dir,
        "excludes" : excludes_console,
        #"includes": ["encodings.*",
                     #"encodings.cp850",
                     #"encodings.cp1252",
                     #"encodings.iso-8859-1"
        #             ],
        "dll_excludes" : dll_excludes,
        }}
        
        )

    zipname = "%s-%s-py2exe.zip" % (name,__version__)
    zipname = opj(DIST_ROOT,zipname)
    zf = zipfile.ZipFile(zipname,'w',zipfile.ZIP_DEFLATED)
    l = rdirlist(dist_dir)
    for fn in l:
        zf.write(opj(dist_dir,fn),opj(name,fn))
    for fn in ['COPYING.txt']:
        zf.write(fn,opj(name,fn))
    zf.close()   

    

if 'raceman' in args:
    
    sys.argv[1:] = ["py2exe"]
    

    console_targets = []
    windows_targets = ['raceman']

    dist_dir = opj(DIST_ROOT,"raceman")
    
    setup(
        name="raceman",
        version=__version__,
        description="Lino Raceman",
        author="Luc Saffre",
        author_email="luc.saffre@gmx.net",
        url=__url__+"/raceman.html",
        long_description="""\
An uncomplete race manager.
Register participants, input arrival times,
generate results report.""",
        windows=[ opj("src", "lino", "apps","raceman",t+".py")
                  for t in windows_targets],
##         packages= ["encodings",
##                    "encodings.cp850",
##                    #"encodings.latin_1"
##                    ],
        options= { "py2exe": {
##         "packages": ["encodings",
##                      "encodings.cp850",
##                      #"encodings.latin_1"
##                      ],
        "includes": ["encodings",
                     "encodings.cp850"],
        "compressed": 1,
        "optimize": 2,
        "dist_dir" : dist_dir,
        "excludes" : excludes,
        "dll_excludes" : dll_excludes        
        }}
        
        )

    script = InnoScript(
        "Raceman",
        dist_dir,\
        version=__version__,
        windows_exe_files= [ fn+".exe" for fn in windows_targets]
        )
    
    script.create()
    script.compile()
    

if 'keeper' in args:
    
    sys.argv[1:] = ["py2exe"]
    
    console_targets = []
    windows_targets = ['keeper']

    dist_dir = opj(DIST_ROOT,"keeper")
    
    setup(
        name="keeper",
        version=__version__,
        description="Lino Document Keeper",
        author="Luc Saffre",
        author_email="luc.saffre@gmx.net",
        url=__url__+"/keeper.html",
        long_description="""\
An uncomplete archive manager.
""",
        #console=[ opj("src", "lino", "apps","keeper",t+".py")
        #          for t in console_targets],
        windows=[ opj("src", "lino", "apps","keeper",t+".py")
                  for t in windows_targets],
##         packages= ["encodings",
##                    "encodings.cp850",
##                    #"encodings.latin_1"
##                    ],
        options= { "py2exe": {
        "includes": ["encodings",
                     "encodings.cp850"],
##                      #"encodings.latin_1"
##                      ],
        "compressed": 1,
        "optimize": 2,
        "dist_dir" : dist_dir,
        "excludes" : excludes,
        "dll_excludes" : dll_excludes
        }}
        
        )

    script = InnoScript(
        "Keeper",
        dist_dir,\
        version=__version__,
        windows_exe_files= [ fn+".exe" for fn in windows_targets]
        )
    
    script.create()
    script.compile()
    

if 'sdist' in args:
    sys.argv[1:] = ["sdist"]
    
    setup(
        name="lino",
        version=__version__,
        description="Lino Framework",
        author="Luc Saffre",
        author_email="luc.saffre@gmx.net",
        url=__url__,
        long_description="""\
Lino is a suite of Python packages for developing business applications for small and medium-sized organisations.
""",
        package_dir = {'': 'src'},
        packages=['lino'],
        )


## distlog.write("done at %s\n\n" % ctime())
## distlog.close()

