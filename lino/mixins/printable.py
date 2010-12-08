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
See :doc:`/admin/printable`

"""
import logging
logger = logging.getLogger(__name__)

import os
import sys
import logging
import cStringIO
import glob
from fnmatch import fnmatch

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string, get_template, select_template, Context, TemplateDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect, Http404

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
#~ from lino import reports
from lino import actions

from lino.utils.babel import default_language, dtos, dtosl, setlang, getattr_lang
from lino.utils import babel 


bm_dict = {}
bm_list = []

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
    templates_name = None
    cache_name = 'cache'
    
    def __init__(self):
        if self.label is None:
            self.label = _(self.__class__.__name__)
        #~ self.templates_dir = os.path.join(settings.PROJECT_DIR,'templates',self.name)
        #~ if self.templates_name is None:
            #~ self.templates_name = self.name
        #~ self.templates_dir = os.path.join(settings.PROJECT_DIR,'doctemplates',self.templates_name or self.name)
        if self.templates_name is None:
            self.templates_name = self.name
        self.templates_dir = os.path.join(settings.MEDIA_ROOT,'webdav','doctemplates',self.templates_name)
        self.templates_url = settings.MEDIA_URL + '/'.join(('webdav','doctemplates',self.templates_name))
        

            
    def __unicode__(self):
        return unicode(self.label)
        
            
    def get_target_parts(self,elem):
        return [self.cache_name, self.name, elem.filename_root() + '-' + str(elem.pk) + self.target_ext]
        
    def get_target_name(self,elem):
        return os.path.join(settings.MEDIA_ROOT,*self.get_target_parts(elem))
        
    def build(self,elem):
        raise NotImplementedError
        
    def before_build(self,elem):
        """Return the target filename if a document needs to be built,
        otherwise return ``None``.
        """
        if not elem.must_build:
            return 
        filename = self.get_target_name(elem)
        if not filename:
            return
        if os.path.exists(filename):
            #~ if not elem.must_rebuild_target(filename,self):
                #~ logger.debug("%s : %s -> %s is up to date",self,elem,filename)
                #~ return
            logger.debug("%s %s -> overwrite existing %s.",self,elem,filename)
            os.remove(filename)
        else:
            dirname = os.path.dirname(filename)
            if not os.path.isdir(dirname):
                if True:
                    raise Exception("Please create yourself directory %s" % dirname)
                else:
                    os.makedirs(dirname)
        logger.debug("%s : %s -> %s", self,elem,filename)
        return filename
        
    def get_template_url(self,elem):
        raise NotImplementedError
        
class DjangoBuildMethod(BuildMethod):

    def get_template(self,elem):
        tpls = elem.get_print_templates(self)
        if len(tpls) == 0:
            raise Exception("No templates defined for %r" % elem)
        #~ logger.debug('make_pisa_html %s',tpls)
        try:
            return select_template(tpls)
        except TemplateDoesNotExist,e:
            raise Exception("No template found for %s (%s)" % (e,tpls))

    def render_template(self,elem,tpl): # ,MEDIA_URL=settings.MEDIA_URL):
        context = dict(
          instance=elem,
          title = unicode(elem),
          MEDIA_URL = settings.MEDIA_ROOT.replace('\\','/') + '/',
        )
        return tpl.render(Context(context))
        
class PisaBuildMethod(DjangoBuildMethod):
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
  
    def get_template_leaf(self,elem):
        tpls = elem.get_print_templates(self)
        #~ if not tpls:
            #~ return
        if len(tpls) != 1:
            raise Exception(
              "%s.get_print_templates() must return exactly 1 template (got %r)" % (
                elem.__class__.__name__,tpls))
        tpl_leaf = tpls[0]
        lang = elem.get_print_language(self)
        if lang != default_language():
            tplfile = os.path.normpath(os.path.join(self.templates_dir,tpl_leaf))
            if not os.path.exists(tplfile):
                lang = default_language()
                #~ tpl = os.path.normpath(os.path.join(self.templates_dir,default_language(),tpl_leaf))
        return lang + '/' + tpl_leaf
        
    def get_template_url(self,elem):
        tpl = self.get_template_leaf(elem)
        return self.templates_url + '/' + tpl
        
    def build(self,elem):
        target = self.before_build(elem)
        if not target:
            return
        tpl_leaf = self.get_template_leaf(elem)
        tplfile = os.path.normpath(os.path.join(self.templates_dir,tpl_leaf))
        self.simple_build(elem,tplfile,target)
        
    def simple_build(self,elem,tpl,target):
        raise NotImplementedError
        
class AppyBuildMethod(SimpleBuildMethod):
  
    """
    Generates .odt files from .odt templates.
    This method doesn't require OpenOffice nor the Python UNO bridge installed. 
    Except in some cases like updating fields
    
    http://appyframework.org/podRenderingTemplates.html
    """
    template_ext = '.odt'  
    templates_name = 'appy' # subclasses use the same templates directory
    
    def simple_build(self,elem,tpl,target):
        context = dict(self=elem,
            dtos=dtos,
            dtosl=dtosl,
            tr=getattr_lang,
            )
        lang = str(elem.get_print_language(self))
        from appy.pod.renderer import Renderer
        logger.debug("appy.pod render %s -> %s using language %r",tpl,target,lang)
        savelang = babel.LANG
        setlang(lang)
        #~ locale.setlocale(locale.LC_ALL,ls)
        #~ Error: unsupported locale setting
        renderer = Renderer(tpl, context, target,**settings.APPY_PARAMS)
        renderer.run()
        setlang(savelang)

class AppyOdtBuildMethod(AppyBuildMethod):
    name = 'appyodt'
    target_ext = '.odt'
    cache_name = 'webdav'

class AppyPdfBuildMethod(AppyBuildMethod):
    """
    Generates .pdf files from .odt templates.
    
    """
    name = 'appypdf'
    target_ext = '.pdf'

class AppyRtfBuildMethod(AppyBuildMethod):
  
    """
    Generates .rtf files from .odt templates.
    """
    name = 'appyrtf'
    target_ext = '.rtf'
    cache_name = 'webdav'


        
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
    cache_name = 'webdav'
    
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
    register_build_method(AppyOdtBuildMethod())
    register_build_method(AppyPdfBuildMethod())
    register_build_method(AppyRtfBuildMethod())
    
if pyratemp:
    register_build_method(RtfBuildMethod())
register_build_method(LatexBuildMethod())

#~ print "%d build methods:" % len(bm_list)
#~ for bm in bm_list:
    #~ print bm


def build_method_choices():
    return [ (pm.name,pm.label) for pm in bm_list]

    
    
def get_template_choices(group,bmname):
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
        logger.warning("get_template_choices() : no matches for (%r,%r) in %s",group,bmname,top)
    return l
            
    
def get_build_method(elem):
    bmname = elem.get_build_method()
    if not bmname:
        raise Exception("%s has no build method" % elem)
    bm = bm_dict.get(bmname,None)
    if bm is None:
        raise Exception("Build method %r doesn't exist. Requested by %r." % (bmname,elem))
    return bm
        

#~ class PrintAction(actions.RedirectAction):
class PrintAction(actions.RowAction):
    """Note that this action should rather be called 
    'Open a printable document' than 'Print'.
    For the user they are synonyms as long as Lino doesn't support server-side printing.
    """
    name = 'print'
    label = _('Print')
    callable_from = None
    #~ needs_selection = True
    
    def run(self,ui,elem,**kw):
        bm = get_build_method(elem)
        if elem.must_build:
            bm.build(elem)
            elem.must_build = False
            elem.save()
            kw.update(refresh=True)
            kw.update(message="%s printable has been build." % elem)
        else:
            kw.update(message="Reused %s printable from cache." % elem)
        target = settings.MEDIA_URL + "/".join(bm.get_target_parts(elem))
        return ui.success_response(open_url=target,**kw)
      
    
class EditTemplateAction(actions.RowAction):
    name = 'tpledit'
    label = _('Edit template')
    
    def run(self,ui,elem,**kw):
        bm = get_build_method(elem)
        target = bm.get_template_url(elem)
        return ui.success_response(open_url=target,**kw)
    
class ClearCacheAction(actions.RowAction):
#~ class ClearCacheAction(actions.UpdateRowAction):
    name = 'clear'
    label = _('Clear cache')
    
    def run(self,ui,elem):
        elem.must_build = True
        elem.save()
        return ui.success_response("%s printable cache has been cleared." % elem,refresh=True)

class PrintableType(models.Model):
    """
    Default value for `templates_group` is the model's `app_label`.
    """
    templates_group = None
    
    class Meta:
        abstract = True
        
    build_method = models.CharField(max_length=20,
      verbose_name=_("Build method"),
      choices=build_method_choices(),blank=True,null=True)
    template = models.CharField(max_length=200,
      verbose_name=_("Template"),
      blank=True,null=True)
    #~ build_method = models.CharField(max_length=20,choices=mixins.build_method_choices())
    #~ template = models.CharField(max_length=200)
    
    @classmethod
    def get_templates_group(cls):
        return cls.templates_group or cls._meta.app_label
        
    def template_choices(cls,build_method):
        #~ print cls, 'template_choices for method' ,build_method
        #~ bm = bm_dict[build_method]
        return get_template_choices(cls.get_templates_group(),build_method)
        #~ return get_template_choices(TEMPLATE_GROUP,build_method)
    template_choices.simple_values = True
    template_choices = classmethod(template_choices)
    
class Printable(models.Model):
    """
    Mixin for Models whose instances can "print" (generate a printable document).
    """
    
    must_build = models.BooleanField(_("must build"),default=True,editable=False)
    
    class Meta:
        abstract = True
        
    @classmethod
    def setup_report(cls,rpt):
        rpt.add_action(PrintAction(rpt))
        rpt.add_action(ClearCacheAction(rpt))
        #~ rpt.add_action(EditTemplateAction(rpt))
        #~ super(Printable,cls).setup_report(rpt)

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
          
    def unused_get_last_modified_time(self):
        """Return a model-specific timestamp that expresses when 
        this model instance has been last updated. 
        Default is to return None which means that existing target 
        files never get overwritten.
        
        """
        return None
        
    def unused_must_rebuild_target(self,filename,pm):
        """When the target document already exists, 
        return True if it should be built again (overriding the existing file. 
        The default implementation is to call :meth:`get_last_modified_time` 
        and return True if it is newer than the timestamp of the file.
        """
        last_modified = self.get_last_modified_time()
        if last_modified is None:
            return False
        mtime = os.path.getmtime(filename)
        #~ st = os.stat(filename)
        #~ mtime = st.st_mtime
        mtime = datetime.datetime.fromtimestamp(mtime)
        if mtime >= last_modified:
            return False
        return True
      
    def get_build_method(self):
        # TypedPrintable  overrides this
        #~ return 'rtf'
        return 'pisa'
        #~ return 'pisa'
        

class TypedPrintable(Printable):
    """
    A TypedPrintable model must define itself a field `type` which is a ForeignKey 
    to a Model that implements PrintableType.
    """
  
    class Meta:
        abstract = True
        
    def get_build_method(self):
        if self.type is None:
            return super(TypedPrintable,self).get_build_method()
        return self.type.build_method
        
    def get_print_templates(self,pm):
        if self.type is None:
            return super(TypedPrintable,self).get_print_templates(self,pm)
            #[self.filename_root() + pm.template_ext]
        assert self.type.template.endswith(pm.template_ext)
        #~ return [ TEMPLATE_GROUP +'/'+self.type.template ]
        return [ self.type.get_templates_group() +'/'+self.type.template ]
        
    def get_print_language(self,pm):
        return self.language


#~ class PrintableTypes(reports.Report):
    #~ column_names = 'name build_method template *'
