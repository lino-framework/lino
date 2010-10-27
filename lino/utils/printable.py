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
See :doc:`/admin/printing`

"""

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

try:
    import appy
except ImportError:
    appy = None
    
try:
    import pyratemp
except ImportError:
    pyratemp = None
        
import lino
from lino import actions
from lino.tools import default_language


bm_dict = {}
bm_list = []
        

class PrintAction(actions.RedirectAction):
    """Note that this action should rather be called 
    'Open a printable document' than 'Print'.
    When Lino one day supports server-side printing, then we'll may have to rename 
    this class.
    """
    name = 'print'
    label = _('Print')
    callable_from = None
    needs_selection = True
  
    def get_target_url(self,elem):
        pm = bm_dict.get(elem.get_build_method(),None)
        if pm is None:
            raise Exception("%r has no build_method (%r)" % (elem,self))
        pm.build(elem)
        return settings.MEDIA_URL + "/".join(pm.get_target_parts(elem))
        
    


class Printable:
    """
    Mixin for Models whose instances can "print" (generate a document).
    """

    def filename_root(self):
        return self._meta.app_label + '.' + self.__class__.__name__
        
    def get_print_language(self,pm):
        return default_language()
        
    def get_print_templates(self,pm):
        """Return a list of filenames of templates for the specified print method.
        Note that for subclasses of :class:`SimpleBuildMethod` this list must either 
        be empty (which means "this item is not printable") or contain a single 
        element.
        """
        return [self.filename_root() + pm.template_ext]
          
    def get_last_modified_time(self):
        """Return a model-specific timestamp that expresses when 
        this model instance has been last updated. If 
        
        """
        return None
        
    def must_rebuild_target(self,filename,pm):
        """Default implementation to decide, when the target document already exists, 
        whether it should be built again. The default implementation is to call
        :meth:`get_last_modified_time` and 
        """
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
      
    def get_build_method(self):
        ## e.g. lino.modlib.notes.Note overrides this
        return 'rtf'
        #~ return 'pisa'
        #~ return 'pisa'
        


class BuildMethod:
    """
    Base class for all print methods.
    A print method encapsulates the process of generating a "document" 
    that inserts data from the database into a template.
    using a given combination of a template parser and post-processor.
    """
    name = None
    label = None
    target_ext = None
    template_ext = None
    #~ button_label = None
    label = None
    
    def __init__(self):
        if self.label is None:
            self.label = _(self.__class__.__name__)
        #~ self.templates_dir = os.path.join(settings.PROJECT_DIR,'templates',self.name)
        self.templates_dir = os.path.join(settings.PROJECT_DIR,'doctemplates',self.name)

            
    def __unicode__(self):
        return unicode(self.label)
            
    def get_target_parts(self,elem):
        return ['cache', self.name, elem.filename_root() + '-' + str(elem.pk) + self.target_ext]
        
    def get_target_name(self,elem):
        return os.path.join(settings.MEDIA_ROOT,*self.get_target_parts(elem))
        
    def build(self,elem):
        raise NotImplementedError
        
    def before_build(self,elem):
        """Return the target filename if a document needs to be built,
        otherwise return ``None``.
        """
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
        except TemplateDoesNotExist,e:
            raise Exception("No template found for %s (%s)" % (tpls,e))

        
    def render_template(self,elem,tpl): # ,MEDIA_URL=settings.MEDIA_URL):
        context = dict(
          instance=elem,
          title = unicode(elem),
          MEDIA_URL = settings.MEDIA_ROOT.replace('\\','/') + '/',
        )
        return tpl.render(Context(context))
        


class PisaBuildMethod(BuildMethod):
    """
    Generates .pdf files from .html templates.
    """
    name = 'pisa'
    target_ext = '.pdf'
    #~ button_label = _("PDF")
    template_ext = '.pisa.html'  
    
    def build(self,elem):
        tpl = self.get_template(elem) 
        filename = self.before_build(elem)
        if filename is None:
            return
        html = self.render_template(elem,tpl) # ,MEDIA_URL=url)
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
        


class SimpleBuildMethod(BuildMethod):
  
    def build(self,elem):
        target = self.before_build(elem)
        if not target:
            return
            
        tpls = elem.get_print_templates(self)
        if not tpls:
            return
        if len(tpls) != 1:
            raise Exception(
              "%s.get_print_templates() must return exactly 1 template (got %r)" % (
                elem.__class__.__name__,tpls))
                
        lang = elem.get_print_language(self)
        tpl = os.path.join(self.templates_dir,lang,tpls[0])
        self.simple_build(elem,tpl,target)
        
    def simple_build(self,elem,tpl,target):
        raise NotImplementedError
        
class AppyBuildMethod(SimpleBuildMethod):
  
    """
    Generates .odt files from .odt templates.
    """
    name = 'appy'
    target_ext = '.odt'
    #~ button_label = _("ODT")
    template_ext = '.odt'  
    
    def simple_build(self,elem,tpl,target):
        context = dict(instance=elem)
        from appy.pod.renderer import Renderer
        renderer = Renderer(tpl, context, target)
        renderer.run()
        
        
class LatexBuildMethod(BuildMethod):
    """
    Generates .pdf files from .tex templates.
    """
    name = 'latex'
    target_ext = '.pdf'
    template_ext = '.tex'  
    
    def simple_build(self,elem,tpl,target):
        context = dict(instance=elem)
        raise NotImplementedError
            
class RtfBuildMethod(SimpleBuildMethod):
    """
    Generates .rtf files from .rtf templates.
    """
  
    name = 'rtf'
    #~ button_label = _("RTF")
    target_ext = '.rtf'
    template_ext = '.rtf'  
    
    def simple_build(self,elem,tpl,target):
        context = dict(instance=elem)
        t = pyratemp.Template(filename=tpl)
        try:
            result = t(**context)
        except pyratemp.TemplateRenderError,e:
            raise Exception(u"%s in %s" % (e,tpl))
        file(target,'wb').write(result)
        


def register_build_method(pm):
    bm_dict[pm.name] = pm
    bm_list.append(pm)
    

if pisa:
    register_build_method(PisaBuildMethod())
if appy:
    register_build_method(AppyBuildMethod())
if pyratemp:
    register_build_method(RtfBuildMethod())
register_build_method(LatexBuildMethod())


def build_method_choices():
    return [ (pm.name,pm.label) for pm in bm_list]

    
    
def template_choices(group,bmname):
    """
    :param:bmname: the name of a build method.
    """
    pm = bm_dict.get(bmname,None)
    #~ pm = get_build_method(build_method)
    if pm is None:
        raise Exception("%r : invalid print method name." % bmname)
    #~ glob_spec = os.path.join(pm.templates_dir,'*'+pm.template_ext)
    top = os.path.join(pm.templates_dir,default_language(),group)
    l = []
    for dirpath, dirs, files in os.walk(top):
        for fn in files:
            if fnmatch(fn,'*'+pm.template_ext):
                if len(dirpath) > len(top):
                    fn = os.path.join(dirpath[len(top)+1:],fn)
                l.append(fn.decode(sys.getfilesystemencoding()))
    if not l:
        lino.log.warning("template_choices() : no matches for (%r,%r) in %s",group,bmname,top)
    return l
            
    