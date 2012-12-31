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
import os
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
E = xghtml.E
    
def site_setup(self):
    """
    Adds a global `jinja_env` attribute to `settings.LINO`
    """
    from lino.utils import auth
    
    self.jinja_env = jinja2.Environment(
        #~ extensions=['jinja2.ext.i18n'],
        loader=jinja2.ChoiceLoader([
          jinja2.FileSystemLoader(os.path.join(self.project_dir,'templates')),
          jinja2.PackageLoader('lino', 'templates')
          ]))
    #~ jinja_env = jinja2.Environment(trim_blocks=False)

    #~ from django.utils import translation

    #~ jinja_env.install_gettext_translations(translation)


    def as_table(action_spec):
        a = settings.LINO.modules.resolve(action_spec)
        ar = a.request(user=auth.AnonymousUser.instance())
        print ar.get_total_count()
        return E.tostring(E.ul(*[E.li(ar.summary_row(obj)) for obj in ar]),method="html")
          
    def as_ul(action_spec):
        a = settings.LINO.modules.resolve(action_spec)
        ar = a.request(user=auth.AnonymousUser.instance())
        return E.tostring(E.ul(*[obj.as_list_item(ar) for obj in ar]),method="html")

    self.jinja_env.globals.update(
            settings=settings,
            # LINO=settings.LINO,
            #~ ui=settings.LINO.ui,
            site=self,
            dtos=babel.dtos,
            dtosl=babel.dtosl,
            as_ul=as_ul,
            as_table=as_table,
            iif=iif,
            unicode=unicode,
            len=len,
            # E=xghtml.E,
            _= _,
    )


def extend_context(context):
    def parse(s):
        #~ print 20121221, s
        #~ return Template(s).render(**context)
        return settings.LINO.jinja_env.from_string(s).render(**context)
    context.update(
        now=datetime.datetime.now(),
        parse=parse,
        requested_language=get_language(),
        )

def render_from_request(request,template_name,**context):
    extend_context(context)
    context.update(request=request)
    template = settings.LINO.jinja_env.get_template(template_name)
    return template.render(**context)


#~ jinja_env.extract_translations()


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
        jt = settings.LINO.jinja_env.get_template(template_name)
        template = DjangoJinjaTemplate(jt)
        return template, origin
        