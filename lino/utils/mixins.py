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

import os
import sys
import logging
import cStringIO
import glob
from fnmatch import fnmatch

from django.conf import settings
from django.template.loader import render_to_string, get_template, select_template, Context, TemplateDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils.translation import ugettext_lazy as _

try:
    import ho.pisa as pisa
    #pisa.showLogging()
except ImportError:
    pisa = None
    
import lino
from lino import actions

try:
    import appy
except ImportError:
    appy = None
    
#~ if False:
    #~ try:
        #~ from lino.utils import appy_pod
    #~ except ImportError:
        #~ appy_pod = None
        
pm_dict = {}
pm_list = []
        
#~ render_methods = {}


class MultiTableBase:
  
    """
    Mixin for Models that use Multi-table inheritance[1].
    Subclassed by :class:`lino.modlib.journals.models.AbstractDocument`
    
    [1] http://docs.djangoproject.com/en/dev/topics/db/models/#multi-table-inheritance
    """
    
    class Meta:
        abstract = True
    
    def get_child_model(self):
        return self.__class__
        
    def get_child_instance(self):
        model = self.get_child_model()
        if model is self.__class__:
            return self
        related_name = model.__name__.lower()
        return getattr(self,related_name)
        


class PrintAction(actions.RedirectAction):
    name = 'print'
    label = _('Print')
    callable_from = None
    needs_selection = True
  
    def get_target_url(self,elem):
        pm = pm_dict.get(elem.get_print_method(),None)
        if pm is None:
            raise Exception("%r has no print_method (%r)" % (elem,self))
        pm.build(elem)
        return settings.MEDIA_URL + "/".join(pm.get_target_parts(elem))
        
    


class Printable:
    """
    Mixin for Models whose instances can "print" (generate a document).
    """

    def filename_root(self):
        return self._meta.app_label + '.' + self.__class__.__name__
        
    def get_print_templates(self,pm):
        return [self.filename_root() + pm.template_ext]
          
    def get_last_modified_time(self):
        return None
        
    def must_rebuild_target(self,filename,pm):
        last_modified = self.get_last_modified_time() 
        if last_modified is None:
            return True
        mtime = os.path.getmtime(filename)
        #~ st = os.stat(filename)
        #~ mtime = st.st_mtime
        mtime = datetime.datetime.fromtimestamp(mtime)
        if mtime >= last_modified:
            return False
        return True
      
    def get_print_method(self):
        ## e.g. lino.modlib.notes.Note overrides this
        return 'pisa'
        #~ return 'pisa'
        


class PrintMethod:
    name = None
    label = None
    target_ext = None
    template_ext = None
    #~ button_label = None
    label = None
    
    def __init__(self):
        if self.label is None:
            self.label = _(self.__class__.__name__)
        self.templates_dir = os.path.join(settings.DATA_DIR,'templates',self.name)

            
    def __unicode__(self):
        return unicode(self.label)
            
    def get_target_parts(self,elem):
        return ['cache', self.name, elem.filename_root() + '-' + str(elem.pk) + self.target_ext]
        
    def get_target_name(self,elem):
        return os.path.join(settings.MEDIA_ROOT,*self.get_target_parts(elem))
        
    def build(self,elem):
        pass
        
    def prepare_cache(self,elem):
        filename = self.get_target_name(elem)
        if not filename:
            return
            
        if os.path.exists(filename):
            if not elem.must_rebuild_target(filename,self):
                lino.log.debug("%s : %s -> %s is up to date",self,elem,filename)
                return
            os.remove(filename)
        else:
            dirname = os.path.dirname(filename)
            if not os.path.isdir(dirname):
                if True:
                    raise Exception("Please create yourself directory %s" % dirname)
                else:
                    os.makedirs(dirname)
        lino.log.debug("%s : %s -> %s", self,elem,filename)
        return filename
        
    def get_template(self,elem):
        tpls = elem.get_print_templates(self)
        if len(tpls) == 0:
            raise Exception("No templates defined for %r" % elem)
        #~ lino.log.debug('make_pisa_html %s',tpls)
        try:
            return select_template(tpls)
        except TemplateDoesNotExist:
            raise Exception("No template found for %s" % tpls)

        
    def render_template(self,elem,tpl): # ,MEDIA_URL=settings.MEDIA_URL):
        url = settings.MEDIA_ROOT.replace('\\','/') + '/'
        context = dict(
          instance=elem,
          title = unicode(elem),
          MEDIA_URL = url,
        )
        return tpl.render(Context(context))
        

#~ class PicturePrintMethod(PrintMethod):
    #~ name = 'picture'
    
    #~ def get_target_name(self,elem):
        #~ return os.path.join(settings.MEDIA_ROOT,*self.get_target_parts(elem))
        
        
class AppyPrintMethod(PrintMethod):
    name = 'appy'
    target_ext = '.odt'
    #~ button_label = _("ODT")
    template_ext = '.odt'  
    def build(self,elem):
        target = self.prepare_cache(elem)
        if not target:
            return
            
        tpls = elem.get_print_templates(self)
        if not tpls:
            return
        if len(tpls) != 1:
            raise Exception(
              "%s.get_print_templates() must return exactly 1 template (got %r)" % (
                elem.__class__.__name__,tpls))
        #~ tpl = self.get_template(elem) 
        tpl = os.path.join(self.templates_dir,tpls[0])
        
        context = dict(instance=elem)
        from appy.pod.renderer import Renderer
        renderer = Renderer(tpl, context, target)
        renderer.run()
        #~ appy_pod.process_pod(template,context,filename)
        
class PisaPrintMethod(PrintMethod):
    name = 'pisa'
    target_ext = '.pdf'
    #~ button_label = _("PDF")
    template_ext = '.pisa.html'  
    
    def build(self,elem):
        tpl = self.get_template(elem) 
        filename = self.prepare_cache(elem)
        if filename is None:
            return
        #~ url = settings.MEDIA_ROOT.replace('\\','/') + '/'
        html = self.render_template(elem,tpl) # ,MEDIA_URL=url)
        #~ html = html.encode("ISO-8859-1")
        html = html.encode("utf-8")
        file(filename+'.html','w').write(html)
        result = cStringIO.StringIO()
        h = logging.FileHandler(filename+'.log','w')
        pisa.log.addHandler(h)
        pdf = pisa.pisaDocument(cStringIO.StringIO(html), result,encoding='utf-8')
        pisa.log.removeHandler(h)
        h.close()
        file(filename,'wb').write(result.getvalue())
        if pdf.err:
            raise Exception("pisa.pisaDocument.err is %r" % pdf.err)
        
        
class RtfPrintMethod(PrintMethod):
  
    name = 'rtf'
    #~ button_label = _("RTF")
    target_ext = '.rtf'
    template_ext = '.rtf'  
    
    def build(self,elem):
        tpl = self.get_template(elem) 
        filename = self.prepare_cache(elem)
        if filename is None:
            return
        result = self.render_template(elem,tpl) # ,MEDIA_URL=url)
        file(filename,'wb').write(result)
        


def register_print_method(pm):
    pm_dict[pm.name] = pm
    pm_list.append(pm)
    

if pisa:
    register_print_method(PisaPrintMethod())
if appy:
    register_print_method(AppyPrintMethod())
register_print_method(RtfPrintMethod())
#~ register_print_method(PicturePrintMethod())


def print_method_choices():
  return [ (pm.name,pm.label) for pm in pm_list]

#~ def get_print_method(name):
    #~ return pm_dict.get(name)

#~ def render_element(elem,fmt):
    #~ rm = render_methods.get(fmt,None)
    
    
    
def template_choices(print_method):
    pm = pm_dict.get(print_method,None)
    #~ pm = get_print_method(print_method)
    if pm is not None:
        glob_spec = os.path.join(pm.templates_dir,'*'+pm.template_ext)
        top = pm.templates_dir
        for dirpath, dirs, files in os.walk(top):
            for fn in files:
                if fnmatch(fn,'*'+pm.template_ext):
                    if len(dirpath) > len(top):
                        fn = os.path.join(dirpath[len(top)+1:],fn)
                    yield fn.decode(sys.getfilesystemencoding())
            
    