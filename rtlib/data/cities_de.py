# -*- coding: utf-8 -*-
# Copyright 2005 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""
"""

import os
import codecs
from HTMLParser import HTMLParser
import formatter
import urllib2

URL="http://de.wikipedia.org/wiki/Liste_der_St%C3%A4dte_in_Deutschland"


class WikipediaCitiesParser(HTMLParser):

    def __init__(self):

        HTMLParser.__init__(self)
        #self._query=q
        #self._city=None
        self._name=None
        self._url=None

    def handle_starttag(self, tag, attrs):
        #print "unknown_starttag", tag
        if tag == "dd":
            assert self._name is None
            #self._city = self._query.appendRowForEditing()
##             self._city = self._query.appendRowForEditing(
##                 nation=self._nation)
            self._name=""
            self._url=None
        elif tag == "a":
            if self._name is not None:
                for attr,v in attrs:
                    if attr == "href":
                        self._url=v

    #def unknown_endtag(self, tag):
    def handle_endtag(self, tag):
        if tag == "dd":
            assert self._name is not None
            name = self._name.replace("\n"," ").strip()
            n=name.rfind("(")
            if n == -1:
                print name
            else:
                print name[:n].strip(), "\t", name[n+1:-1]
            #a=name.split("(")
            #if len(a) == 2:
            #    print a[0].strip(), "\t", a[1][:-1]
            #else:
            #    print name
            #print self._name.replace("\n"," ").strip()
            #print repr(self._name)
            #print name
            self._name = None
            self._url = None

    def handle_data(self, data):
        #if "Dr" in data:
        #    print data
        if self._name is not None:
            self._name += data
        #else:
        #    print data


if __name__ == "__main__":

    print "name\tbundesland_name"
    parser=WikipediaCitiesParser()
    if False:
        #f=urllib.urlopen(URL)
        opener = urllib2.build_opener()
        opener.addheaders = [
            ('User-agent', 'Mozilla/5.0')
            ]
        f=opener.open(URL)
    else:
        f = codecs.open('cities_de.html','rt',"utf-8")
    parser.feed(f.read())
    parser.close()
    f.close()
