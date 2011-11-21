#coding: latin1
## Copyright 2003-2008 Luc Saffre

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
"""
from lino.misc.tsttools import TestCase, main
from lino.htgen import Document
from lino.reports.reports import ListReport,LEFT,RIGHT
from lino.reports.datatypes import PRICE


class InvoiceReport(ListReport):
    data=(
        ("pcd.fsc","Fujitsu-Siemens Esprimo","756,50"),
        ("mon.lcd.fsc",'Fujitsu-Siemens Monitor 19"',"370,80"),
        ("acc.cdr",'CDRW 10 pcs',"12,20"),
        )
    width=50
    def setupReport(self):
        self.addColumn(label="Item no.",width=11)
        self.addColumn(label="Description"),
        #self.addColumn( label="Qty", width=3),
        #self.addColumn(label="Unit price", width=12),
        self.addColumn(label="Price", datatype=PRICE),

class Case(TestCase):

    def test01(self):
        
        doc=Document("Invoice no %d" % 123)
        doc.h1(doc.title)
        doc.par("Tallinn, 10. juuni 2006. a.",align="RIGHT")
        doc.report(InvoiceReport())
        
        if True:
            spoolFile = self.addTempFile("84.html",showOutput=True)
            doc.saveas(spoolFile)
        
        
        self.assertEquivalentHtml(doc.toxml(), """
<html><head>
<title>Invoice no 123</title>
<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">
<meta name="KEYWORDS" content="">
<meta name="GENERATOR" content="lino.htgen">
<meta name="author" content="">
<meta name="date" content="None"><head>
<BODY>
<H1>Invoice no 123</H1>
<P align="RIGHT">Tallinn, 10. juuni 2006. a.</P>
<TABLE>
<COLGROUP><COL width="11*"/><COL width="27*"/><COL width="12*"/></COLGROUP>
<THEAD><TR>
<TH align="LEFT" valign="TOP">Item no.</TH>
<TH align="LEFT" valign="TOP">Description</TH>
<TH align="RIGHT" valign="TOP">Price</TH>
</TR></THEAD>
<TBODY>
<TR>
<TD align="LEFT" valign="TOP">pcd.fsc</TD>
<TD align="LEFT" valign="TOP">Fujitsu-Siemens Esprimo</TD>
<TD align="RIGHT" valign="TOP">756,50</TD>
</TR>
<TR>
<TD align="LEFT" valign="TOP">mon.lcd.fsc</TD>
<TD align="LEFT" valign="TOP">Fujitsu-Siemens Monitor 19&quot;</TD>
<TD align="RIGHT" valign="TOP">370,80</TD>
</TR>
<TR>
<TD align="LEFT" valign="TOP">acc.cdr</TD>
<TD align="LEFT" valign="TOP">CDRW 10 pcs</TD>
<TD align="RIGHT" valign="TOP">12,20</TD>
</TR>
</TBODY></TABLE></BODY>
</html>""")
    
        
        

                
if __name__ == '__main__':
    main()

