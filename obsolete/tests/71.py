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

import os
opj = os.path.join

from lino.misc.tsttools import TestCase, main

from lino.gendoc.html_site import StaticHtmlDocument


class Case(TestCase):

    def test01(self):
        "Location arithmetics"
        root = StaticHtmlDocument()
        self.assertEqual(root.location,"")
        self.assertEqual(root.filename(),"index.html")
        
        foo=root.addChild(location="foo")
        self.assertEqual(foo.location,"foo")
        self.assertEqual(foo.filename(),"index.html")
        
        bar=foo.addChild(location="bar")
        self.assertEqual(bar.location,"foo/bar")
        self.assertEqual(bar.filename(),"index.html")
        
        self.assertEqual(root.urlto(foo),"foo/index.html")
        self.assertEqual(root.urlto(bar),"foo/bar/index.html")
        
        self.assertEqual(foo.urlto(root),"../index.html")
        self.assertEqual(foo.urlto(bar),"bar/index.html")
        
        self.assertEqual(bar.urlto(root),"../../index.html")
        self.assertEqual(bar.urlto(foo),"../index.html")
        
    
if __name__ == '__main__':
    main()

