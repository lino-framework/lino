import unittest
import sys,os

import lino.plugins.system
import lino.plugins.addrbook
import lino.plugins.news
import lino.plugins.sdk
import lino.plugins.quotes
import lino.plugins.sales
import lino.plugins.products


from lino.lib import tsttools

suite = tsttools.alltests()

runner = unittest.TextTestRunner()

lino.startup()

runner.run(suite)
   
