#import sys
#sys.path.append("..")

import lino.demo
#from lino.plugins import system
#from lino.plugins import addrbook
#from lino.plugins import community
#from lino.plugins import sdk
#from lino.plugins import quotes

from lino.tools import *
from lino import mysql_dbd 
from lino import sql_dbd 

#app = lino.demoapp.app
writer = BufferWriter()
host = sql_dbd.ConsoleHost(writer)
lino.demo.app.Startup(mysql_dbd.Connection(host))
lino.demo.app.initdb()
#app.initdemo()

print writer.unwrite()
