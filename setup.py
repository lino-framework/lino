# setup.py
"""

don't use setup.py to install the lino package. Just checkout the
latest source to some directory and add it to your PYTHONPATH.

"""
from distutils.core import setup
import py2exe
import glob

## setup(name="lino",
## 		version='0.6.1',
## 		description="Lino Database Application Framework",
##       author="Luc Saffre",
##       author_email="luc.saffre@gmx.net",
##       url="http://lino.sourceforge.net",
## 		long_description="A collection of command-line tools",
## 		packages=['lino',
##  					 'lino.adamo',
##  					 'lino.agui',
##  					 'lino.examples',
##  					 'lino.quix',
##  					 'lino.sprl',
##  					 'lino.wxgui',
##  					 'lino.misc',
##  					 'lino.sdoc'],
## 		scripts=glob.glob("scripts\\*.py"),
## 		package_dir = {'': 'src'}
## )

from lino import __version__

dll_excludes = ['cygwin1.dll']
excludes = [ "pywin", "pywin.debugger", "pywin.debugger.dbgcon",
             "pywin.dialogs", "pywin.dialogs.list",
             "Tkconstants","Tkinter","tcl",
             "wx"
             ]

setup(name="timtools",
      version=__version__,
      description="Lino TIM tools",
      author="Luc Saffre",
      author_email="luc.saffre@gmx.net",
      url="http://lino.sourceforge.net",
      long_description="A collection of command-line tools",
      console=[r"src\lino\scripts\pds2pdf.py",
               r"src\lino\scripts\prn2pdf.py",
               r"src\lino\scripts\openmail.py"],
      options= { "py2exe": { 
                 "excludes" : excludes
                 }}
      
)
