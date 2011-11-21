## Copyright 2003-2006 Luc Saffre

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

import tempfile
import os
opj = os.path.join

from lino.misc.tsttools import TestCase, main

from lino.apps.pinboard.pinboard_demo import startup
from lino.apps.pinboard import pinboard_tables as tables

from lino.gendoc.html import HtmlDocument
from lino.adamo.dbreports import QueryReport


class Case(TestCase):
    todo="HtmlDocument is broken"

    def setUp(self):
        TestCase.setUp(self)
        self.sess = startup(withJokes=True)

    def tearDown(self):
        self.sess.shutdown()

    def test01(self):
        #targetDir = opj(tempfile.gettempdir(), "reports_test_2")
        #targetDir = opj(r"c:\temp","linoweb")
        #targetDir="temp"
        #print targetDir
        
        root = HtmlDocument(title="The first Linoweb",
                            stylesheet="wp-admin.css")
        mnu = root.addMenu()
                            
        
        ds = self.sess.query(tables.Nation,
                             pageLen=50,
                             orderBy="name")
        rpt = QueryReport(ds)
        doc=root.addChild(location="nations",
                          name=rpt.name,
                          title=rpt.getLabel())
        doc.report(rpt)
        mnu.addLink(doc)

        if True:
            ds = self.sess.query(tables.Quote,"quote author.name id",
                                 pageLen=50,
                                 orderBy="id")
            rpt = QueryReport(ds)
            doc=root.addChild(location="quotes",
                              name=rpt.name,
                              title=rpt.getLabel())
            doc.report(rpt)
            mnu.addLink(doc)
                

            
        files=root.save(self.sess,
                        opj(self.tempDir,"gendoc","2"))
        self.addTempFile(files[0],showOutput=True)
        for fn in files[1:]:
            self.addTempFile(fn)
        
    
if __name__ == '__main__':
    main()

