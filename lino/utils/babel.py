## Copyright 2009-2010 Luc Saffre
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

"""

Funktion `add_babel_field`
um das Definieren von Babel-Feldern zu erleichtern.
Wird z.B. wie folgt aufgerufen::

    add_babel_field(ContractType,'name')
  

"""

import logging
logger = logging.getLogger(__name__)

import locale

from django.db import models
from django.conf import settings

#~ from lino.tools import default_language

def default_language():
    """
    Returns the default language of this website
    as defined by :setting:`LANGUAGE_CODE` in your :xfile:`settings.py`.
    """
    #~ from django.conf import settings
    return settings.LANGUAGE_CODE[:2]
    


LANG = None

LONG_DATE_FMT = {
  None: '%A, %d. %B %Y',
  'de': '%A, %d. %B %Y',
  'fr': '%A %d %B %Y',
  'et': '%A, %d. %B %Y.a.',
}

SHORT_DATE_FMT = {
  None: '%y-%m-%d',
  'de': '%d.%m.%Y',
  'et': '%d.%m.%Y',
  'fr': '%d/%m/%Y',
}


#~ from lino.utils import lc2locale

def lc2locale(lang,country):
    """
    Convert a combination of `lang` and `country` codes to 
    a platform-dependant locale setting to be used for 
    :func:`locale.setlocale`.
    Thanks to 
    http://www.gossamer-threads.com/lists/python/bugs/721929
    and
    http://msdn.microsoft.com/en-us/library/hzz3tw78
    """
    if sys.platform == 'win32': # development server
        if lang == 'fr':
            if country == 'BE': return 'french-belgian'
            return 'french'
        if lang == 'de':
            if country == 'BE': return 'german-belgian'
            return 'german'
        raise NotImplementedError("lc2locale(%r,%r)" % (lang,country))
    else:
        return lang+'_'+country
        


def dtos(d):
    return d.strftime(SHORT_DATE_FMT[LANG])

def dtosl(d):
    return d.strftime(LONG_DATE_FMT[LANG])
    
def setlang(lang):
    global LANG
    LANG = lang
    if lang is None:
        locale.setlocale(locale.LC_ALL,'')
    else:
        country = settings.LANGUAGE_CODE[3:]
        locale.setlocale(locale.LC_ALL,lc2locale(lang,country))
    
        #~ save_ls = locale.getlocale()
        #~ ls = lc2locale(lang,country)
        #~ ls = 'de-DE' # de_DE
        #~ print ls
        #~ logger.debug("appy.pod render %s -> %s using locale=%r",tpl,target,ls)
        #~ locale.setlocale(locale.LC_ALL,'')
    
    
def getattr_lang(obj,name,*args):
    """
    return the value of the specified attribute `name` of `obj`,
    but if `obj` also has a multi-language version of that 
    attribute for the current language, then prefer this attribute's 
    value if it is not blank.
    
    This is to be used in multilingual document templates.

    For example in a document template of a Contract you may now use the following expression::

      getattr_lang(self.type,'name')

    When generating a Contract in french (:attr:`dsbe.Contract.language` is ``fr``), 
    the expression will return :attr:`dsbe.ContractType.name_fr` if this field is not blank. 
    Otherwise (if the contract's language is not ``fr``, 
    of if this contract's type's `name_fr` field is blank) 
    it returns :attr:`dsbe.ContractType.name`.

    Not tested for other field types than CHAR.
    
    Topic: :doc:`/topics/babel`.
    
    See also :doc:`/blog/2010/1207`.
    
    """
    if LANG != default_language():
        v = getattr(obj,name+"_"+LANG,None)
        if v:
            return v
    return getattr(obj,name,*args)
        
babelattr = getattr_lang
    
def add_babel_field(model,name,*args,**kw):
#~ def add_lang_field(model,name,lang,*args,**kw):
    f = model._meta.get_field(name)
    #~ if not f.blank:
    kw.update(blank=True)
    if isinstance(f,models.CharField):
        kw.update(max_length=f.max_length)
    for lang in settings.BABEL_LANGS:
        kw.update(verbose_name=f.verbose_name + ' ('+lang+')')
        newfield = f.__class__(*args,**kw)
        model.add_to_class(name + '_' + lang,newfield)


def babel_values(name,**kw):
    d = { name : kw.get(default_language())}
    for lang in settings.BABEL_LANGS:
        v = kw.get(lang,None)
        if v is not None:
            d[name+'_'+lang] = v
    return d

