## Copyright 2005 Luc Saffre 

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

import os
import codecs
#from htmllib import HTMLParser
from HTMLParser import HTMLParser
import formatter

from lino.schemas.sprl.tables import Nations

dataDir = os.path.dirname(__file__)


class WikipediaCitiesParser(HTMLParser):

    def __init__(self, q):

        #w = formatter.NullWriter()
        #fmt = formatter.AbstractFormatter(w)
        #HTMLParser.__init__(self,fmt)
        HTMLParser.__init__(self)
        self._query=q
        self._city=None
        self._name=None
        self._url=None


    
    #def unknown_starttag(self, tag, attrs):
    def handle_starttag(self, tag, attrs):
        #print "unknown_starttag", tag
        if tag == "dd":
            assert self._city is None
            self._city = self._query.appendRowForEditing()
##             self._city = self._query.appendRowForEditing(
##                 nation=self._nation)
            self._name=""
            self._url=None
        elif tag == "a":
            if self._city is not None:
                for attr,v in attrs:
                    if attr == "href":
                        self._url=v
            
    #def unknown_endtag(self, tag):
    def handle_endtag(self, tag):
        if tag == "dd":
            if self._city is not None:
                assert self._name is not None
                self._name = self._name.replace("\n"," ").strip()
                self._city.name=self._name
                self._city.commit()
                #print self._city
                self._city = None

    def handle_data(self, data):
        #if "Dr" in data:
        #    print data
        if self._city is not None:
            self._name += data



def populate(q):
    de = q.getSession().peek(Nations,'de')
    parser=WikipediaCitiesParser(de.cities)
    #f = open(os.path.join(dataDir,'cities_de.htm'))
    f = codecs.open(os.path.join(dataDir,'cities_de.htm'),'rb',"utf-8")
    #cities = de.cities
    #print cities
    parser.feed(f.read())
    parser.close()
    f.close()
    

    
