# -*- coding: utf-8 -*-
## Copyright 2011 Luc Saffre
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

A setup funtion for Sphinx documentaton.

Used by the Lino documentation::

  from lino.utils.sphinx import setup

"""

import os
import lino


#~ from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


def srcref(mod):
    """
    Return the `source file name` for usageby Sphinx's ``srcref`` role.
    Returns None if the source file is empty (which happens e.g. for __init__.py 
    files whose only purpose is to mark a package).
    
    >>> from lino.utils import log
    >>> print srcref(log)
    lino/utils/log.py

    >>> from lino import utils
    >>> print srcref(utils)
    lino/utils/__init__.py
    
    >>> from lino.management import commands
    >>> print srcref(commands)
    None

    """
    if not mod.__name__.startswith('lino.'): 
        return
    srcref = mod.__file__
    if srcref.endswith('.pyc'):
        srcref = srcref[:-1]
    if os.stat(srcref).st_size == 0:
        return 
    srcref = srcref[len(lino.__file__)-17:]
    srcref = srcref.replace(os.path.sep,'/')
    return srcref
    


def autodoc_skip_member(app, what, name, obj, skip, options):
    if name != '__builtins__':
        #~ print 'autodoc_skip_member', what, repr(name), repr(obj)
    
        if what == 'class':
            if name.endswith('MultipleObjectsReturned'):
                return True
            if name.endswith('DoesNotExist'):
                return True
                
            #~ if isinstance(obj,ObjectDoesNotExist) \
              #~ or isinstance(obj,MultipleObjectsReturned): 
                #~ return True
        
    #~ if what == 'exception': 
        #~ print 'autodoc_skip_member',what, repr(name), repr(obj), skip
        #~ return True
        

SIDEBAR = """
(This module's source code is available at :srcref:`/%s`)

"""  

#~ SIDEBAR = """
#~ .. sidebar:: Use the source, Luke

  #~ We generally recommend to also consult the source code.
  #~ This module's source code is available at
  #~ :srcref:`/%s.py`

#~ """  


    
def autodoc_add_srcref(app,what,name,obj,options,lines):
    if what == 'module':
        s = srcref(obj)
        if s:
            #~ srcref = name.replace('.','/')
            s = (SIDEBAR % s).splitlines()
            s.reverse()
            for ln in s:
                lines.insert(0,ln)
            #~ lines.insert(0,'')
            #~ lines.insert(0,'(We also recommend to read the source code at :srcref:`/%s.py`)' % name.replace('.','/'))
    

def setup(app):
    app.add_object_type(directivename='xfile',rolename='xfile',
      indextemplate='pair: %s; file')
    app.add_object_type(directivename='setting',rolename='setting',
      indextemplate='pair: %s; setting')
    #~ app.add_object_type(directivename='model',rolename='model',
      #~ indextemplate='pair: %s; model')
    #~ app.add_object_type(directivename='field',rolename='field',
      #~ indextemplate='pair: %s; field')
    app.add_object_type(directivename='table',rolename='table',
      indextemplate='pair: %s; table')
    app.add_object_type(directivename='modattr',rolename='modattr',
      indextemplate='pair: %s; model attribute')
    app.add_object_type(directivename='model',rolename='model',
      indextemplate='pair: %s; model')
    #app.connect('build-finished', handle_finished)
    
    app.connect('autodoc-skip-member',autodoc_skip_member)
    app.connect('autodoc-process-docstring', autodoc_add_srcref)


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()

