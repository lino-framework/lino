# coding: latin1
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


"""
Logical columns (row attributes) versus physical columns (atoms)

"""
import types

from lino.misc.tsttools import TestCase, main
from lino.apps.pinboard.pinboard_demo import startup
from lino.apps.pinboard.pinboard_tables import Project
#from lino.reports import DataReport


class Case(TestCase):
    """
    selecting "WHERE x is NULL"
    """

    def setUp(self):
        TestCase.setUp(self)
        self.sess = startup()

    def tearDown(self):
        self.sess.shutdown()


    def test01(self):
        PROJECTS = self.sess.query(Project)
        qry = PROJECTS.query("id super.id title")
        self.assertEqual(len(qry),10)
        qry.show(columnWidths="5 5 20")
        #rpt=self.sess.createDataReport(qry,columnWidths="5 5 20")
        #self.sess.showReport(rpt)
        
        s = self.getConsoleOutput()
        #print s
        self.assertEqual(s,"""\
Projects
========
id   |super|title               
     |.id  |                    
-----+-----+--------------------
1    |     |Project 1           
2    |     |Project 2           
3    |     |Project 3           
4    |1    |Project 1.1         
5    |1    |Project 1.2         
6    |1    |Project 1.3         
7    |6    |Project 1.3.1       
8    |6    |Project 1.3.2       
9    |8    |Project 1.3.2.1     
10   |8    |Project 1.3.2.2     
""")
        
        """
        The Python value None is principally translated as NULL to SQL.

        For example, specifying super=None will select only the
        top-level projects (whose super is NULL): """
        
        qry = self.sess.query(Project,"id title", super=None)
        self.assertEqual(len(qry),3)
        qry.show(columnWidths="5 20")
        #self.sess.showQuery(qry,columnWidths="5 20")
        #rpt=self.sess.createDataReport(qry,columnWidths="5 20")
        #self.sess.showReport(rpt)
        
        s = self.getConsoleOutput()
        #print s
        self.assertEqual(s,"""\
Projects (super=None)
=====================
id   |title               
-----+--------------------
1    |Project 1           
2    |Project 2           
3    |Project 3           
""")


##         """

##         Samples are sticky properties: once set, the get inherited by
##         all children.  To clear a sample of a child, you must
##         explicitly set it to Datasource.ANY_VALUE.
        
##         Example: you want to use the ds from above as parent for a new
##         ds because you want to inherit columnNames. But now you want to
##         see them all, not only the top-level projects.  So you must
##         clear the "super=None" condition.

##         """
        
##         ds = ds.query(orderBy="title",super=ds.ANY_VALUE)
##         self.assertEqual(len(ds),10)

        
##         """
##         Calling
##         http://localhost:8080/lino/db/PROJECTS?v=std
##         must show only the projects with super=None
##         """

##         rpt=self.sess.getViewReport(Project,"std")
##         #ds = self.sess.view(Project,"std")
##         self.assertEqual(len(rpt),3)

        
        
##         try:
##             rpt=self.sess.getViewReport(Project,"nonExistingViewName")
##             self.fail("failed to raise exception for bad viewName")
##         except KeyError:
##             pass
        
        



if __name__ == '__main__':
    main()

