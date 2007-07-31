## Copyright 2005-2007 Luc Saffre

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

from lino.console import syscon

from lino.misc.etc import ispure

_userLang = None
_messages = {}

def _(text_en):
    if _userLang is None:
        return text_en
    try:
        return _messages[text_en][_userLang]
    except KeyError:
        #print "No translation to %s for %r." % (_userLang,text_en)
        return text_en

def setUserLang(lang):
    global _userLang
    if _userLang == "en":
        _userLang = None
    else:
        _userLang = lang
    
def itr(text_en,**kw):
    for v in kw.values():
        assert ispure(v)
    _messages[text_en] = kw




import locale
setUserLang(locale.getdefaultlocale()[0][:2])
#print _userLang
