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

_userLang = None
_messages = {}

import locale
_userLang = locale.getdefaultlocale()[0][:2]
if _userLang == "en":
    _userLang = None
#print _userLang

def _(text_en):
    if _userLang is None:
        return text_en
    try:
        return _messages[text_en][_userLang]
    except KeyError:
        from lino.ui import console
        console.warning(
            "No translation to %s for %s." % (
            _userLang,
            repr(text_en)))
            
        return text_en

def setUserLang(lang):
    global _userLang
    _userLang = lang
    
def itr(text_en,**kw):
    _messages[text_en] = kw

