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
import calendar

import lino


#~ from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.util.compat import Directive

from lino.utils import babel

#~ class ScreenshotDirective(directives.images.Image):
    #~ """
    #~ Directive to insert a screenshot.
    #~ """
    #~ def run(self):
        #~ assert len(self.arguments) == 1
        #~ # name = '/../gen/screenshots/' + self.arguments[0]
        #~ name = '/gen/screenshots/' + self.arguments[0]
        #~ self.arguments = [name]
        #~ (image_node,) = directives.images.Image.run(self)
        #~ return [image_node]





def srcref(mod):
    """
    Return the `source file name` for usage by Sphinx's ``srcref`` role.
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

    >>> from lino_welfare import settings
    >>> print srcref(settings)
    lino_welfare/settings.py

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
        

#~ SIDEBAR = """
#~ (This module's source code is available at :srcref:`/%s`)

#~ """  
#~ SIDEBAR = """
#~ (source code: :srcref:`/%s`)

#~ """  

SIDEBAR = """
(:srcref:`source code </%s>`)

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
    

import jinja2

templates = dict()
templates['calendar.rst'] = """
====
{{year}}
====

{{intro}}

.. |br| raw:: html

   <br />   

.. |sp| raw:: html

   <span style="color:white;">00</span>

{{calendar}}


"""

JINJA_ENV = jinja2.Environment(
    #~ extensions=['jinja2.ext.i18n'],
    loader=jinja2.DictLoader(templates))


class InsertInputDirective(Directive):
    has_content = True
    def get_rst(self):
        raise NotImplementedErrro()
        
    def run(self):
        out = self.get_rst()
        #~ print '-' * 50
        #~ print out
        #~ print '-' * 50
        #~ sys.exit()
        self.state_machine.insert_input(out.splitlines(),out)
        return []

    
class BlogIndexDirective(InsertInputDirective):
    """
    Directive to insert a year's calendar
    """
    #~ required_arguments = 1
    
    def get_rst(self):
        #~ year = self.arguments[0]
        env = self.state.document.settings.env
        
        intro = '\n'.join(self.content)
        dn  = os.path.dirname(env.doc2path(env.docname))
        year = os.path.split(dn)[-1]
        year = int(year)
        
        days = set()
            
        for (dirpath, dirnames, filenames) in os.walk(dn):
            for fn in filenames:
                if fn.endswith('.rst'):
                    s = fn[:-4]
                    if len(s) == 4:
                        days.add(s)
        
        
        tpl = JINJA_ENV.get_template('calendar.rst')
        
        cal = calendar.Calendar()
        text = ''
        
        for month in range(1,13):
            
            text += """        
            
.. |M%02d| replace::  **%s**""" % (month,babel.monthname(month))
            
            weeknum = None
            for day in cal.itermonthdates(year,month):
                iso_year,iso_week,iso_day = day.isocalendar()
                if iso_week != weeknum:
                    text += "\n  |br|"
                    weeknum = iso_week
                if day.month == month:
                    label = "%02d" % day.day
                    docname = "%02d%02d" % (day.month,day.day)
                    if year == iso_year and docname in days:
                        text += " :doc:`%s <%s>` " % (label,docname)
                    else:
                        text += ' ' + label + ' '
                else:
                    text += ' |sp| '
                
            
            
        text += """
        
===== ===== =====
|M01| |M02| |M03|
|M04| |M05| |M06|
|M07| |M08| |M09|
|M10| |M11| |M12|
===== ===== =====
        
        """
        
        
        return tpl.render(
            calendar=text,intro=intro,env=env,
            year=year,
            days=days)
        

def setup(app):
    """
    The Sphinx setup function used for Lino-related documentation trees.
    """
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
    app.add_object_type(directivename='screenshot',rolename='screen',
      indextemplate='pair: %s; screenshot')
    app.add_object_type(directivename='modattr',rolename='modattr',
      indextemplate='pair: %s; model attribute')
    app.add_object_type(directivename='model',rolename='model',
      indextemplate='pair: %s; model')
    #app.connect('build-finished', handle_finished)
    
    app.connect('autodoc-skip-member',autodoc_skip_member)
    app.connect('autodoc-process-docstring', autodoc_add_srcref)

    #~ app.add_node(blogindex)
    #~ app.add_node(blogindex,html=(visit_blogindex,depart_blogindex))
    app.add_directive('blogindex', BlogIndexDirective)
    #~ app.add_directive('screenshot', ScreenshotDirective)
    #~ app.add_config_value('screenshots_root', '/screenshots/', 'html')

    app.add_stylesheet('linodocs.css')

    