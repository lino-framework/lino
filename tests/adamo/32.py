# coding: latin1

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
Some tests on getDemoDB()
"""

import types
import unittest

from lino.adamo.datatypes import DataVeto
from lino.adamo import Table

from lino.schemas.sprl import demo
from lino.schemas.sprl.tables import *


class Case(unittest.TestCase):

    def setUp(self):
        
        self.sess = demo.beginSession()

    def tearDown(self):
        self.sess.shutdown()


    def test01(self):
        
        self.sess.setBabelLangs('en')
        
        rpt = self.sess.report()
        rpt.addVurtColumn(
            meth=lambda rpt: rpt.crow.getTableName(),
            label="TableName",
            width=20)
        def count(rpt):
            return len(self.sess.query(rpt.crow.__class__))
        rpt.addVurtColumn(
            meth=count,
            width=5, halign=rpt.RIGHT,
            label="Count")
        rpt.addVurtColumn(
            meth=lambda rpt: self.sess.query(rpt.crow.__class__)[0],
            when=lambda rpt: rpt.cellValues[1]>0,
            label="First",
            width=20)
        rpt.addVurtColumn(
            meth=lambda rpt: self.sess.query(rpt.crow.__class__)[-1],
            when=lambda rpt: rpt.cellValues[1]>0,
            label="Last",
            width=20)
        
        rpt.beginReport()
        for t in self.sess.schema.getTableList():
            rpt.processRow(t)
        rpt.endReport()
            

if __name__ == '__main__':
    unittest.main()

