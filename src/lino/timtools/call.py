#coding: latin1
"""
A file timtools.bat can do::

  python -c "from lino.timtools import call" %1 %2 %3 %4 %5 %6

which is equivalent to 

"""

import sys

## import os,sys
## (dirname,filename) = os.path.split(__file__)
## scriptsdir = os.path.abspath(os.path.join(dirname,"..","..","..","scripts"))
## sys.path.insert(0,scriptsdir)
## import sys.argv[1]

from lino.misc.my_import import my_import

mod = my_import("lino.timtools." + sys.argv[1])
mod.main(sys.argv[2:])
