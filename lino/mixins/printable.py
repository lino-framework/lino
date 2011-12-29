# -*- coding: UTF-8 -*-
## Copyright 2009-2011 Luc Saffre
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
import traceback
import cStringIO
import datetime
import glob
from fnmatch import fnmatch

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string, get_template, select_template, Context, TemplateDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils.encoding import force_unicode

import lino
from lino import dd

from lino.utils import iif
from lino.utils import babel 
#~ from lino.utils import call_optional_super
from lino.utils.choosers import chooser
from lino.utils.appy_pod import setup_renderer
from lino.tools import makedirs_if_missing



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
        
def filename_root(elem):
    return elem._meta.app_label + '.' + elem.__class__.__name__

def model_group(elem):
    return elem._meta.app_label + '/' + elem.__class__.__name__



bm_dict = {}
bm_list = []


class BuildMethod:
    """
    Base class for all build methods.
    A build method encapsulates the process of generating a 
    "printable document" that inserts data from the database 
    into a template, using a given combination of a template 
    parser and post-processor.
    """
    name = None
    label = None
    target_ext = None
    template_ext = None
    #~ button_label = None
    label = None
    templates_name = None
    cache_name = 'cache'
    #~ webdav = False
    default_template = ''
    
    use_webdav = False
    """
    Whether this build method results is an editable file.
    For example, `.odt` files are considered editable 
    while `.pdf` files aren't.
    
    In that case the target will be in a webdav folder 
    and the print action will respond 
    `open_davlink_url` instead of the usual `open_url`,
    which extjs3 ui will implement by calling `Lino.davlink_open()`
    instead of the usual `window.open()`.
    
    When :attr:`lino.Lino.use_davlink` is `False`,
    this setting still influences the target path
    of resulting files, but the clients 
    will not automatically recognize them as 
    webdav-editable URLs.
    """
    
    def __init__(self):
        if self.label is None:
            self.label = _(self.__class__.__name__)
        #~ self.templates_dir = os.path.join(settings.PROJECT_DIR,'templates',self.name)
        #~ if self.templates_name is None:
            #~ self.templates_name = self.name
        #~ self.templates_dir = os.path.join(settings.PROJECT_DIR,'doctemplates',self.templates_name or self.name)
        if self.templates_name is None:
            self.templates_name = self.name
        #~ self.old_templates_dir = os.path.join(settings.LINO.webdav_root,'doctemplates',self.templates_name)
        #~ self.templates_url = settings.LINO.webdav_url + '/'.join(('doctemplates',self.templates_name))
        

            
    def __unicode__(self):
        return unicode(self.label)
        
    def get_target_parts(self,action,elem):
        "used by `get_target_name`"
        return [self.cache_name, self.name, filename_root(elem) + '-' + str(elem.pk) + self.target_ext]
        
    def get_target_name(self,action,elem):
        "return the output filename to generate on the server"
        if self.use_webdav and settings.LINO.use_davlink:
            return os.path.join(settings.LINO.webdav_root,*self.get_target_parts(action,elem))
        return os.path.join(settings.MEDIA_ROOT,*self.get_target_parts(action,elem))
        
    def get_target_url(self,action,elem,ui):
        "return the url that points to the generated filename on the server"
        if self.use_webdav and settings.LINO.use_davlink:
            return settings.LINO.webdav_url + "/".join(self.get_target_parts(action,elem))
        #~ return settings.MEDIA_URL + "/".join(self.get_target_parts(action,elem))
        return ui.media_url(*self.get_target_parts(action,elem))
            
    def build(self,action,elem):
        raise NotImplementedError
        
    #~ def get_template_url(self,action,elem):
        #~ raise NotImplementedError
        
class DjangoBuildMethod(BuildMethod):

    def get_template(self,action,elem):
        tpls = action.get_print_templates(self,elem)
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
    
    def build(self,action,elem):
        tpl = self.get_template(action,elem) 
        filename = action.before_build(self,elem)
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
        fd = file(filename,'wb')
        fd.write(result.getvalue())
        fd.close()
        if pdf.err:
            raise Exception("pisa.pisaDocument.err is %r" % pdf.err)
        return os.path.getmtime(filename)
        
        
        

class SimpleBuildMethod(BuildMethod):
  
    def get_group(self,elem):
        #~ return 'doctemplates/' + self.templates_name + '/' + elem.get_templates_group()
        return elem.get_templates_group()
  
    def get_template_leaf(self,action,elem):
      
        tpls = action.get_print_templates(self,elem)
        #~ if not tpls:
            #~ return
        if len(tpls) != 1:
            raise Exception(
              "%s.get_print_templates() must return exactly 1 template (got %r)" % (
                elem.__class__.__name__,tpls))
        tpl_leaf = tpls[0]
        lang = elem.get_print_language(self)
        if lang != babel.DEFAULT_LANGUAGE:
            name = tpl_leaf[:-len(self.template_ext)] + "_" + lang + self.template_ext
            from lino.utils.config import find_config_file
            if find_config_file(name,self.get_group(elem)):
                return name
        return tpl_leaf
            #~ tplfile = os.path.normpath(os.path.join(self.templates_dir,lang,tpl_leaf))
            #~ if not os.path.exists(tplfile):
                #~ lang = babel.DEFAULT_LANGUAGE
        #~ return lang + '/' + tpl_leaf
        
    #~ def get_template_url(self,action,elem):
        #~ tpl = self.get_template_leaf(action,elem)
        #~ return self.templates_url + '/' + tpl
        
    def build(self,action,elem):
        #~ if elem is None:
            #~ return
        from lino.utils.config import find_config_file
        target = action.before_build(self,elem)
        if not target:
            return
        tpl_leaf = self.get_template_leaf(action,elem)
        tplfile = find_config_file(tpl_leaf,self.get_group(elem))
        if not tplfile:
            raise Exception("No file %s / %s" % (self.get_group(elem),tpl_leaf))
        #~ tplfile = os.path.normpath(os.path.join(self.templates_dir,tpl_leaf))
        return self.simple_build(elem,tplfile,target)
        
    def simple_build(self,elem,tpl,target):
        raise NotImplementedError
        
class AppyBuildMethod(SimpleBuildMethod):
    """
    Base class for Build Methods that use `.odt` templates designed
    for :term:`appy.pod`.
    
    http://appyframework.org/podRenderingTemplates.html
    """
    
    template_ext = '.odt'  
    templates_name = 'appy' # subclasses use the same templates directory
    default_template = 'Default.odt'
    
    def simple_build(self,elem,tpl,target):
        #~ from lino.models import get_site_config
        from appy.pod.renderer import Renderer
        renderer = None
        context = dict(self=elem,
            dtos=babel.dtos,
            dtosl=babel.dtosl,
            dtomy=babel.dtomy,
            babelattr=babel.babelattr,
            babelitem=babel.babelitem,
            tr=babel.babelitem,
            iif=iif,
            settings=settings,
            #~ restify=restify,
            #~ site_config = get_site_config(),
            site_config = settings.LINO.site_config,
            _ = _,
            #~ knowledge_text=fields.knowledge_text,
            )
        lang = str(elem.get_print_language(self))
        logger.info(u"appy.pod render %s -> %s (language=%r,params=%s",
            tpl,target,lang,settings.LINO.appy_params)
        savelang = babel.get_language()
        babel.set_language(lang)
        #~ locale.setlocale(locale.LC_ALL,ls)
        #~ Error: unsupported locale setting
        renderer = Renderer(tpl, context, target,**settings.LINO.appy_params)
        setup_renderer(renderer)
        #~ renderer.context.update(restify=debug_restify)
        renderer.run()
        babel.set_language(savelang)
        return os.path.getmtime(target)
        

class AppyOdtBuildMethod(AppyBuildMethod):
    """
    Generates .odt files from .odt templates.
    
    This method doesn't require OpenOffice nor the 
    Python UNO bridge installed
    (except in some cases like updating fields).
    """
    name = 'appyodt'
    target_ext = '.odt'
    cache_name = 'userdocs'
    #~ cache_name = 'webdav'
    use_webdav = True

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
    cache_name = 'userdocs'
    #~ cache_name = 'webdav'
    use_webdav = True

class AppyDocBuildMethod(AppyBuildMethod):
    """
    Generates .doc files from .odt templates.
    """
    name = 'appydoc'
    target_ext = '.doc'
    cache_name = 'userdocs'
    #~ cache_name = 'webdav'
    use_webdav = True

        
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
    cache_name = 'userdocs'
    #~ cache_name = 'webdav'
    
    def simple_build(self,elem,tpl,target):
        context = dict(instance=elem)
        t = pyratemp.Template(filename=tpl)
        try:
            result = t(**context)
        except pyratemp.TemplateRenderError,e:
            raise Exception(u"%s in %s" % (e,tpl))
        fd = file(target,'wb')
        fd.write(result)
        fd.close()
        return os.path.getmtime(target)
        


def register_build_method(pm):
    bm_dict[pm.name] = pm
    bm_list.append(pm)
 
register_build_method(AppyOdtBuildMethod())
register_build_method(AppyPdfBuildMethod())
register_build_method(AppyRtfBuildMethod())   
register_build_method(LatexBuildMethod())
register_build_method(PisaBuildMethod())
register_build_method(RtfBuildMethod())

#~ print "%d build methods:" % len(bm_list)
#~ for bm in bm_list:
    #~ print bm


def build_method_choices():
    return [ (pm.name,pm.label) for pm in bm_list]

    
    
def get_template_choices(elem,bmname):
    """
    :param:bmname: the name of a build method.
    """
    bm = bm_dict.get(bmname,None)
    if bm is None:
        raise Exception("%r : invalid print method name." % bmname)
    from lino.utils.config import find_config_files
    files = find_config_files('*' + bm.template_ext,bm.get_group(elem))
    l = []
    for name in files.keys():
        # ignore babel variants: 
        # e.g. ignore "foo_fr.odt" if "foo.odt" exists 
        # but don't ignore "my_template.odt"
        basename = name[:-len(bm.template_ext)]
        chunks = basename.split('_')
        if len(chunks) > 1:
            basename = '_'.join(chunks[:-1])
            if files.has_key(basename + bm.template_ext):
                continue
        l.append(name)
    l.sort()
    if not l:
        logger.warning("get_template_choices() : no matches for (%r,%r)",'*' + bm.template_ext,bm.get_group(elem))
    return l

def old_get_template_choices(group,bmname):
    """
    :param:bmname: the name of a build method.
    """
    pm = bm_dict.get(bmname,None)
    if pm is None:
        raise Exception("%r : invalid print method name." % bmname)
    #~ glob_spec = os.path.join(pm.templates_dir,'*'+pm.template_ext)
    top = os.path.join(pm.templates_dir,babel.DEFAULT_LANGUAGE,group)
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
class BasePrintAction(dd.RowAction):
  
    def before_build(self,bm,elem):
        """Return the target filename if a document needs to be built,
        otherwise return ``None``.
        """
        filename = bm.get_target_name(self,elem)
        if not filename:
            return
        if os.path.exists(filename):
            logger.info(u"%s %s -> overwrite existing %s.",bm,elem,filename)
            os.remove(filename)
        else:
            makedirs_if_missing(os.path.dirname(filename))
        logger.debug(u"%s : %s -> %s", bm,elem,filename)
        return filename
        
        
class PrintAction(BasePrintAction):
    """Note that this action should rather be called 
    'Open a printable document' than 'Print'.
    For the user they are synonyms as long as 
    Lino doesn't support server-side printing.
    """
    name = 'print'
    label = _('Print')
    #~ callable_from = None
    callable_from = (dd.GridEdit,dd.ShowDetailAction)
    
    #~ needs_selection = True
    
    def before_build(self,bm,elem):
        #~ if not elem.must_build:
        if elem.build_time:
            return
        return BasePrintAction.before_build(self,bm,elem)
            
    def get_print_templates(self,bm,elem):
        return elem.get_print_templates(bm,self)
        
    def run_(self,request,ui,elem,**kw):
        bm = get_build_method(elem)
        #~ if elem.must_build:
        if not elem.build_time:
            t = bm.build(self,elem)
            if t is None:
                raise Exception("%s : build() returned None?!")
                #~ kw.update(message=_("%s printable has been built.") % elem)
            else:
                elem.build_time = datetime.datetime.fromtimestamp(t)
                #~ bm.build(self,elem)
                #~ elem.must_build = False
                elem.save()
                kw.update(refresh=True)
                kw.update(message=_("%s printable has been built.") % elem)
        else:
            kw.update(message=_("Reused %s printable from cache.") % elem)
        url = bm.get_target_url(self,elem,ui)
        if bm.use_webdav and settings.LINO.use_davlink:
            kw.update(open_davlink_url=request.build_absolute_uri(url))
        else:
            kw.update(open_url=url)
        return kw
        #~ return rr.ui.success_response(open_url=target,**kw)
        
    def run(self,rr,elem,**kw):
        kw = self.run_(rr.request,rr.ui,elem,**kw)
        return rr.ui.success_response(**kw)
      
class DirectPrintAction(BasePrintAction):
    """
    A Print Action that uses a hard-coded template.
    """
    #~ def __init__(self,rpt,name,label,bmname,tplname):
    def __init__(self,name,label,tplname=None,build_method=None):
        BasePrintAction.__init__(self,name,label)
        #~ self.bm =  bm_dict.get(build_method or settings.LINO.preferred_build_method)
        self.build_method = build_method
        self.tplname = tplname
        
    def get_print_templates(self,bm,elem):
        #~ assert bm is self.bm
        if self.tplname:
            return [ self.tplname + bm.template_ext ]
        return elem.get_print_templates(bm,self)
        #~ return super(DirectPrintAction,self).get_print_templates(bm,elem)
        
        
    def run(self,rr,elem,**kw):
        bm =  bm_dict.get(self.build_method or settings.LINO.site_config.default_build_method)
        #~ if self.tplname:
            #~ if not self.tplname.endswith(bm.template_ext):
                #~ raise Exception("Invalid template for build method %r" % bm.name)
        bm.build(self,elem)
        #~ target = settings.MEDIA_URL + "/".join(bm.get_target_parts(self,elem))
        #~ return rr.ui.success_response(open_url=target,**kw)
        url = bm.get_target_url(self,elem,rr.ui)
        if bm.use_webdav and settings.LINO.use_davlink:
            url = rr.request.build_absolute_uri(url)
            kw.update(open_davlink_url=url)
        else:
            kw.update(open_url=url)
        return rr.ui.success_response(**kw)
    
#~ class EditTemplateAction(dd.RowAction):
    #~ name = 'tpledit'
    #~ label = _('Edit template')
    
    #~ def run(self,rr,elem,**kw):
        #~ bm = get_build_method(elem)
        #~ target = bm.get_template_url(self,elem)
        #~ return rr.ui.success_response(open_url=target,**kw)
    
class ClearCacheAction(dd.RowAction):
    """
    Defines the :guilabel:`Clear cache` button on a Printable record.
    """
    name = 'clear'
    label = _('Clear cache')
    
    def disabled_for(self,obj,request):
        #~ print "ClearCacheAction.disabled_for()", obj
        #~ if obj.must_build:
        if not obj.build_time:
            return True
    
    def run(self,rr,elem):
        t = elem.get_cache_mtime()
        if t is not None and t != elem.build_time:
            #~ logger.info("%r != %r", elem.get_cache_mtime(),elem.build_time)
            rr.confirm(1,
                _("This will discard all changes in the generated file."),
                _("Are you sure?"))
            logger.info("Got confirmation to discard changes in %s", elem.get_cache_filename())
        #~ else:
            #~ logger.info("%r == %r : no confirmation", elem.get_cache_mtime(),elem.build_time)
          
        #~ elem.must_build = True
        elem.build_time = None
        elem.save()
        return rr.ui.success_response("%s printable cache has been cleared." % elem,refresh=True)

class PrintableType(models.Model):
    """
    Base class for models that specify the :attr:`TypedPrintable.type`.
    """
    
    templates_group = None
    """
    Default value for `templates_group` is the model's full name.
    """
    
    class Meta:
        abstract = True
        
    build_method = models.CharField(max_length=20,
      verbose_name=_("Build method"),
      choices=build_method_choices(),blank=True)
    """
    The name of the build method to be used.
    The list of choices for this field is static, but depends on 
    which additional packages are installed.
    """
    
    template = models.CharField(max_length=200,
      verbose_name=_("Template"),
      blank=True)
    """
    The name of the file to be used as template.
    The list of choices for this field depend on the :attr:`build_method`.
    Ending must correspond to the :attr:`build_method`.
    """
    
    #~ build_method = models.CharField(max_length=20,choices=mixins.build_method_choices())
    #~ template = models.CharField(max_length=200)
    
    @classmethod
    def get_templates_group(cls):
        #~ return cls.templates_group or cls._meta.app_label
        return cls.templates_group # or full_model_name(cls)
        
    @chooser(simple_values=True)
    def template_choices(cls,build_method):
        #~ from lino.models import get_site_config
        if not build_method:
            #~ build_method = get_site_config().default_build_method 
            #~ build_method = settings.LINO.config.default_build_method 
            build_method = settings.LINO.site_config.default_build_method 
        return get_template_choices(cls,build_method)
    
class Printable(object):
    """
    Mixin for Models whose instances can "print" (generate a printable document).
    """
  
    def get_print_language(self,pm):
        return babel.DEFAULT_LANGUAGE
        
    def get_templates_group(self):
        return model_group(self)
        
  
class CachedPrintable(models.Model,Printable):
    
    #~ must_build = models.BooleanField(_("must build"),default=True,editable=False)
    build_time = models.DateTimeField(_("build time"),null=True,editable=False)
    """
    Timestamp of the built target file. Contains `None` 
    if no build hasn't been called yet.
    """
    
    class Meta:
        abstract = True
        
    @classmethod
    def setup_report(cls,rpt):
        #~ call_optional_super(CachedPrintable,cls,'setup_report',rpt)
        rpt.add_action(PrintAction())
        rpt.add_action(ClearCacheAction())

    def get_print_templates(self,bm,action):
        """Return a list of filenames of templates for the specified build method.
        Returning an empty list means that this item is not printable. 
        For subclasses of :class:`SimpleBuildMethod` the returned list 
        may not contain more than 1 element.
        """
        #~ return [ filename_root(self) + bm.template_ext ]
        if bm.default_template:
            return [ bm.default_template ]
        return [ 'Default' + bm.template_ext ]
          
    def get_build_method(self):
        # TypedPrintable  overrides this
        #~ return 'rtf'
        #~ from lino.models import get_site_config
        #~ return get_site_config.default_build_method 
        return settings.LINO.site_config.default_build_method
        #~ return settings.LINO.preferred_build_method 
        #~ return 'pisa'
        
    def get_cache_filename(self):
        # TODO: too stupid that we must instantate an Action here...
        a = PrintAction()
        bm = get_build_method(self)
        return bm.get_target_name(a,self)
        
    def get_cache_mtime(self):
        filename = self.get_cache_filename()
        if not filename: return None
        try:
            t = os.path.getmtime(filename)
        except OSError,e:
            return None
        return datetime.datetime.fromtimestamp(t)
        
        

class TypedPrintable(CachedPrintable):
    """
    A TypedPrintable model must define itself a field `type` which is a ForeignKey 
    to a Model that implements :class:`PrintableType`.
    
    Alternatively you can override :meth:`get_printable_type` 
    if you want to name the field differently. An example of 
    this is :attr:`lino.modlib.sales.models.SalesDocument.imode`.
    """
    
    type = NotImplementedError
    """
    Override this by a ForeignKey field.
    """
  
    class Meta:
        abstract = True
        
    def get_printable_type(self):
        return self.type
        
    def get_templates_group(self):
        ptype = self.get_printable_type()
        if ptype is None:
            return super(TypedPrintable,self).get_templates_group()
        return ptype.get_templates_group()
        
    def get_build_method(self):
        ptype = self.get_printable_type()
        if ptype is None:
            return super(TypedPrintable,self).get_build_method()
        if ptype.build_method:
            return ptype.build_method
        return settings.LINO.site_config.default_build_method 
        
    def get_print_templates(self,bm,action):
        ptype = self.get_printable_type()
        if ptype is None:
            return super(TypedPrintable,self).get_print_templates(bm,action)
        tplname = ptype.template or bm.default_template
        if not tplname.endswith(bm.template_ext):
            raise Exception(
              "Invalid template %r configured for %s %r (expected filename ending with %r)" %
              (tplname,ptype.__class__.__name__,unicode(ptype),bm.template_ext))
        return [ tplname ]
        #~ return [ ptype.get_templates_group() + '/' + ptype.template ]
        
    def get_print_language(self,bm):
        return self.language



  
import cgi


class Listing(CachedPrintable):
    """
    Abstract base class for all Listings. 
    A Listing is a printable report that requires some parameters given by the user.
    Subclasses must implement the :meth:`body` method.
    Each time a user asks to print a Listing, Lino will create a new record.
    """
    #~ template_name = 'Listing.odt'
    template_name = None
    build_method = None
    
    class Meta:
        abstract = True
    
    date = models.DateField(
        blank=True,null=True,
        verbose_name=_("Date"))
    header_html = dd.RichTextField(_("Header"),editable=False)
    footer_html = dd.RichTextField(_("Footer"),editable=False)
    body_html = dd.RichTextField(_("Body"),editable=False)
        
    #~ title = models.CharField(max_length=200,
      #~ verbose_name=_("Title"),
      #~ blank=True)
    #~ """
    #~ The title of the listing.
    #~ """
    
    @classmethod
    def unused_setup_report(model,rpt):
        u"""
        """
        # to not call call_optional_super(Listing,self,'setup_report',rpt)
        #~ rpt.get_action('listing').label = model.__name__
        rpt.add_action(DirectPrintAction('print',_("Print"),
          model.template_name,model.build_method))
        #~ rpt.add_action(InititateListing('listing',_("Print"),'listing.odt'))
        
    def __unicode__(self):
        return force_unicode(self.title)
        #~ return self.get_title()
        
    #~ def get_templates_group(self):
        #~ return ''
        
    def get_title(self):
        return self._meta.verbose_name # "Untitled Listing"
    title = property(get_title)
        
    def header(self):
        return '<p align="center"><b>%s</b></p>' % cgi.escape(self.title)
        
    def footer(self):
        html = '<td align="left">%s</td>' % 'left footer'
        html += '<td align="right">Page X of Y</td>'
        html = '<table width="100%%"><tr>%s</tr></table>' % html
        return html
        
    def body(self):
        """
        To be implemented by subclasses.
        Build the XHTML content of the listing to be printed.
        """
        raise NotImplementedError
        
    #~ def preview(self,request):
        #~ return self.header() + self.body() + self.footer()
    #~ preview.return_type = fields.HtmlBox(_("Preview"))
    def save(self,*args,**kw):
        self.header_html = self.header()
        self.footer_html = self.footer()
        self.body_html = self.body()
        super(Listing,self).save(*args,**kw)
    
    def get_preview(self,request):
        return self.header_html + self.body_html + self.footer_html
    preview = dd.VirtualField(dd.HtmlBox(_("Preview")),get_preview)
    
    
class InitiateListing(dd.InsertRow):
    """
    This is the (otherwise invisible) action which is used 
    for the main menu entry of a :class:`Listing`.
    """
    callable_from = tuple()
    name = 'listing'
    #~ label = _("Initiate")
    key = None
    
    def get_action_title(self,rh):
        return _(u"Initiate Listing «%s»") % self.actor.model._meta.verbose_name
  
    def get_button_label(self):
        return self.actor.model._meta.verbose_name
        
class Listings(dd.Table):
    model = Listing
    
    def init_label(self):
        return _(u"Listings «%s»") % self.model._meta.verbose_name
        
    def setup_actions(self):
        #~ print 'lino.mixins.printable.Listings.setup_actions : ', self.model
        alist = []
        #~ if len(self.detail_layouts) > 0:
        if True:
            self.detail_action = dd.ShowDetailAction(self)
            alist.append(self.detail_action)
            alist.append(dd.SubmitDetail())
            alist.append(InitiateListing(self,label=self.model._meta.verbose_name)) # replaces InsertRow
            alist.append(dd.SubmitInsert())
            self.default_action = dd.GridEdit(self)
            #~ alist.append(self.default_action)
        alist.append(dd.DeleteSelected())
        self.set_actions(alist)
        
    