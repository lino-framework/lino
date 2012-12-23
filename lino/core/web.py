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

"""

"""

import cgi
import datetime
import jinja2

#~ from jinja2 import Template

#~ from jinja2 import Environment, PackageLoader

from django.conf import settings
from django.utils.translation import get_language
from django.utils.translation import ugettext_lazy as _

from lino.utils import babel
from lino.utils import iif
from lino.utils.xmlgen import html as xghtml
    

jinja_env = jinja2.Environment(
    loader=jinja2.PackageLoader('lino', 'templates'))
#~ jinja_env = jinja2.Environment(trim_blocks=False)


def as_ul(action_spec):
    a = settings.LINO.modules.resolve(action_spec)
    ar = a.request()
    E = xghtml.E
    return E.tostring(E.ul(*[obj.as_list_item(ar) for obj in ar]))

jinja_env.globals.update(
        settings=settings,
        # LINO=settings.LINO,
        #~ ui=settings.LINO.ui,
        site=settings.LINO,
        as_ul=as_ul,
        iif=iif,
        len=len,
        # E=xghtml.E,
        _= _,
)





#~ def build_page_template(site):
    # return Template('\n'.join(list(bootstrap_page_template(site))))
    #~ return jinja_env.from_string('\n'.join(list(bootstrap_page_template(site))))



def extend_context(context):
    def parse(s):
        #~ print 20121221, s
        #~ return Template(s).render(**context)
        return jinja_env.from_string(s).render(**context)
    context.update(
        now=datetime.datetime.now(),
        parse=parse,
        )

def render_node(request,node,template_name='node.html',**context):
  
    extend_context(context)
    
    context.update(
        node=node,
        request=request,
        #~ cgi=cgi,
        #~ babel=babel,
        requested_language=get_language(),
        #~ title=cgi.escape(node.title)
        )
        
    #~ context.update(parse=parse)
        
    #~ context.update(sidebar=settings.LINO.get_sidebar_html(**context))
    #~ context.update(header=settings.LINO.get_header_html(**context))
    #~ context.update(footer=settings.LINO.get_footer_html(**context))
        
    #~ def parse(s):
        #~ return self.parse(s,**context)
    #~ context.update(parse=parse)
    
    #~ if not obj.body:
        #~ context.update(body=obj.abstract)
        
    template = jinja_env.get_template(template_name)
        
    return template.render(**context)



class DjangoJinjaTemplate:
  
    def __init__(self,jt):
        self.jt = jt
  
    def render(self, context):
        # flatten the Django Context into a single dictionary.
        context_dict = {}
        for d in context.dicts:
            context_dict.update(d)
        extend_context(context_dict)
        context_dict.update(request=None)
        return self.jt.render(context_dict)  
  
  
from django.template.loaders import app_directories

class Loader(app_directories.Loader):  
  
    is_usable = True

    def load_template(self, template_name, template_dirs=None):
        source, origin = self.load_template_source(template_name, template_dirs)
        jt = jinja_env.get_template(template_name)
        template = DjangoJinjaTemplate(jt)
        return template, origin
        