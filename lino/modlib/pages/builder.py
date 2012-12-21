# -*- coding: UTF-8 -*-
## Copyright 2012 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.



#~ import datetime
from django.conf import settings
#~ from lino.utils.instantiator import Instantiator

from lino import dd
from lino.utils import babel
from lino.utils.restify import restify
from lino.management.commands.makedocs import doc2rst

pages = dd.resolve_app('pages')

PAGES = {}

def pagekey(self): 
    return (self.language,self.ref)

class PageBuilderMeta(type):
    def __new__(meta, classname, bases, classDict):
        classDict.setdefault('ref',classname.lower())
        cls = type.__new__(meta, classname, bases, classDict)
        #~ if not classDict.has_key('ref'):
            #~ cls.ref = classname.lower()
        if cls.ref == 'index':
            cls.ref = ''
        if (not cls.language) or cls.language in babel.AVAILABLE_LANGUAGES:
            PAGES[pagekey(cls)] = cls
        return cls


def objects():
    global PAGES
    for cls in PAGES.values():
        if cls is not Page:
            if cls.raw_html:
                body = cls.__doc__
            else:
                body = restify(doc2rst(cls.__doc__))
            yield pages.page(cls.ref,cls.language,cls.title,body,special=cls.special)
            #~ yield pages.Page(
                #~ ref=cls.ref,
                #~ language=cls.language,
                #~ title=cls.title,
                #~ body=restify(cls.__doc__))
    PAGES = {}

class Page(object):
    __metaclass__ = PageBuilderMeta
    language = ''
    ref = ''
    title = ''
    raw_html = False
    special = False

    
