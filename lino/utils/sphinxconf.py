# -*- coding: utf-8 -*-
## Copyright 2011-2012 Luc Saffre
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

Sphinx setup used to build the Lino documentation.

Thanks to 

- `Creating reStructuredText Directives 
  <http://docutils.sourceforge.net/docs/howto/rst-directives.html>`_


"""

import os
import sys
import calendar
import datetime
from StringIO import StringIO

import lino

from django.conf import settings

#~ from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.util.compat import Directive

from lino.utils import babel
from lino.utils import rstgen

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
    """
    Base class for directives that work by generating rst markup
    to be forwarded to `state_machine.insert_input()`.
    """
    has_content = True
    def get_rst(self):
        raise NotImplementedErrro()
        
    def run(self):
        out = self.get_rst()
        env = self.state.document.settings.env
        #~ print env.docname
        #~ print '-' * 50
        #~ print out
        #~ print '-' * 50
        #~ sys.exit()
        self.state_machine.insert_input(out.splitlines(),out)
        return []



class Py2rstDirective(InsertInputDirective):
    """
    This works, but is not used.
    """
    def get_rst(self):
        code = '\n'.join(self.content)
        old = sys.stdout
        buffer = StringIO()
        sys.stdout = buffer
        exec(code,{})
        sys.stdout = old
        return buffer.getvalue()
        
        
class TextImageDirective(InsertInputDirective):
    """
    See :doc:`/blog/2013/0116` for documentation.
    """
    required_arguments = 1
    final_argument_whitespace = True
    option_spec = dict(scale=directives.unchanged)
    #~ optional_arguments = 4
    
    def get_rst(self):
        #~ print 'MainBlogIndexDirective.get_rst()'
        #~ env = self.state.document.settings.env
        #~ print self.arguments, self.options, self.content
        left = '\n'.join(self.content)
        right = ''
        for arg in self.arguments[0].split():
            right += '.. figure:: %s\n' % arg
            for i in self.options.items():
                right += "  :%s: %s\n" % i
            right += "\n  %s\n\n" % arg
            #~ right += "\n  \n\n" % arg
            
        return rstgen.table(["",""],[[left,right]],show_headers=False)
    
class ComplexTableDirective(InsertInputDirective):
    """
    The `complextable` directive is used to create tables
    with complex cell content
    
    Usage example::
    
      .. complextable::
    
        A1
        <NEXTCELL>
        A2
        <NEXTROW>
        B1
        <NEXTCELL>
        B2
        
    
    Result:
    
    .. complextable::
    
        A1
        <NEXTCELL>
        A2
        <NEXTROW>
        B1
        <NEXTCELL>
        B2
        
        
    See :doc:`/blog/2013/0116` for documentation.
    """
    required_arguments = 0
    final_argument_whitespace = True
    option_spec = dict(header=directives.flag)
    #~ option_spec = dict(scale=unchanged)
    #~ optional_arguments = 4
    
    def get_rst(self):
        #~ print 'MainBlogIndexDirective.get_rst()'
        #~ env = self.state.document.settings.env
        #~ print self.arguments, self.options, self.content
        cellsep = '<NEXTCELL>'
        rowsep = '<NEXTROW>'
        if len(self.arguments) > 0:
            cellsep = self.arguments[0]
        if len(self.arguments) > 1:
            rowsep = self.arguments[1]
        
        content = '\n'.join(self.content)
        rows = []
        
        for row in content.split(rowsep):
            rows.append([cell.strip() for cell in row.split(cellsep)])
              
        if 'header' in self.options:
            return rstgen.table(rows[0],rows[1:])
            
        return rstgen.table(["",""],rows,show_headers=False)








class Year(object):
    """
    A :class:`Year` instance is created for each 
    `blogger_year` directive.
    """
    #~ _instances = dict()
    #~ def __init__(self,env,blogname,starting_year):
    #~ def __init__(self,env,blogname,year):
    def __init__(self,env):
        """
        :docname: the name of the document containing the `main_blogindex` directive
        :starting_year: all years before this year will be pruned
        """
        
        blogname, year, index = env.docname.rsplit('/',3)
        if index != 'index':
            raise Exception("Allowed only in /<blogname>/<year>/index.rst files")
        self.year = int(year)
        
        #~ print "20130113 Year.__init__", blogname, self.year
        #~ self.blogname = blogname
        self.days = set()
        #~ self.years = set()
        #~ self.starting_year = int(starting_year)
        top = os.path.dirname(env.doc2path(env.docname))
        #~ print top
        for (dirpath, dirnames, filenames) in os.walk(top):
            del dirnames[:] # don't descend another level
            #~ unused, year = dirpath.rsplit(os.path.sep,2)
            #~ year = int(year)
            #~ assert year in self.years
            for fn in filenames:
                if len(fn) == 8 and fn.endswith('.rst'):
                    d = docname_to_day(self.year,fn[:-4])
                    self.days.add(d)
                    #~ self.years.add(s)
                        
        #~ self.years = sorted(self.years)
        if not hasattr(env,'blog_instances'):
            env.blog_instances = dict()
        years = env.blog_instances.setdefault(blogname,dict())
        years[self.year] = self
                        
        
        
"""
docs/conf.py
docs/blog/index.rst --> contains a main_blogindex directive (hidden toctree)
docs/blog/2013/index.rst --> contains a blogger_year directive (calendar)
docs/blog/2013/0107.rst --> a blog entry
docs/blog/2010/0107.rst

"""
        
   
    
class MainBlogIndexDirective(InsertInputDirective):
    """
    Directive to insert a blog master archive page toctree
    """
    #~ required_arguments = 1
  
    def get_rst(self):
        #~ print 'MainBlogIndexDirective.get_rst()'
        env = self.state.document.settings.env
        intro = '\n'.join(self.content)
        #~ dn  = os.path.dirname(env.doc2path(env.docname))
        #~ year = os.path.split(dn)[-1]
        blogname, index = env.docname.rsplit('/',2)
        if index != 'index':
            raise Exception("Allowed only inside index.rst file")
        #~ blog = Blog.get_or_create(env,blogname,self.arguments[0])
        text = intro
        text += """

.. toctree::
    :maxdepth: 2

"""
        years = list(env.blog_instances.get(blogname).values())
        def f(a,b): 
            return cmp(a.year,b.year)
        years.sort(f)
        for blogger_year in years:
        #~ for year in blog.years:
            text += """
    %d/index""" % blogger_year.year
  
        text += "\n"
        #~ print text
        return text
   
   
   

class YearBlogIndexDirective(InsertInputDirective):
    """
    Directive to insert a year's calendar
    """
    #~ required_arguments = 1
    
      
    def get_rst(self):
        #~ year = self.arguments[0]
        env = self.state.document.settings.env
        
        
        #~ dn  = os.path.dirname(env.doc2path(env.docname))
        #~ year = os.path.split(dn)[-1]
        blogger_year = Year(env)
        #~ blog = Blog.get_or_create(env,blogname)
        
        tpl = JINJA_ENV.get_template('calendar.rst')
        
        intro = '\n'.join(self.content)
        cal = calendar.Calendar()
        text = ''
        
        for month in range(1,13):
            
            text += """        
            
.. |M%02d| replace::  **%s**""" % (month,babel.monthname(month))
            
            weeknum = None
            for day in cal.itermonthdates(blogger_year.year,month):
                iso_year,iso_week,iso_day = day.isocalendar()
                if iso_week != weeknum:
                    text += "\n  |br|"
                    weeknum = iso_week
                if day.month == month:
                    label = "%02d" % day.day
                    docname = "%02d%02d" % (day.month,day.day)
                    if blogger_year.year == iso_year and day in blogger_year.days:
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
        
        text += """

.. toctree::
    :hidden:
    :maxdepth: 2
    
"""
        
        days = sorted(blogger_year.days)
        for day in days:
            text += """
    %02d%02d""" % (day.month,day.day)
        
        return tpl.render(
            calendar=text,
            intro=intro,
            year=blogger_year.year,
            days=blogger_year.days)
        

def docname_to_day(year,s):
    #~ print fn
    month = int(s[:2])
    day = int(s[2:])
    return datetime.date(year,month,day)
  
  
#~ class ChangedDirective(InsertInputDirective):
  
    #~ def get_rst(self):
        #~ env = self.state.document.settings.env
        #~ blogname, year, monthday = env.docname.rsplit('/',3)
        #~ # raise Exception("Allowed only in blog entries")
        
        #~ year = int(year)
        #~ day = docname_to_day(year,monthname)
        
        #~ if not hasattr(env,'changed_items'):
            #~ env.changed_items = dict()
        #~ env.changed_items
        #~ for item in self.content:
            #~ entries = env.changed_items.setdefault(item,dict())
            #~ entries.setdefault(env.docname)
        

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
    #~ app.add_directive('changed', ChangedDirective)
    app.add_directive('blogger_year', YearBlogIndexDirective)
    app.add_directive('blogger_index', MainBlogIndexDirective)
    app.add_directive('textimage', TextImageDirective)
    app.add_directive('complextable', ComplexTableDirective)
    app.add_directive('py2rst', Py2rstDirective)
    #~ app.add_directive('screenshot', ScreenshotDirective)
    #~ app.add_config_value('screenshots_root', '/screenshots/', 'html')

    app.add_stylesheet('linodocs.css')

    