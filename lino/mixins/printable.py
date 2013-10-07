# -*- coding: UTF-8 -*-
## Copyright 2009-2013 Luc Saffre
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

from __future__ import unicode_literals

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
from django.utils.translation import string_concat

from djangosite.dbutils import dtomy

import lino
#~ from lino import dd

from lino.core import actions
from lino.core import fields
from lino.core import dbutils
from lino.utils import iif, moneyfmt
#~ from north import dbutils
#~ from lino.utils import call_optional_super
from lino.utils.choosers import chooser
from lino.utils.appy_pod import Renderer
from lino.core.model import Model
from lino.mixins.duplicable import Duplicable

from lino.utils.media import MediaFile
from lino.utils.media import TmpMediaFile
from lino.utils.pdf import merge_pdfs


def decfmt(v,places=2,**kw):
    """
    Format a Decimal value.
    Like :func:`lino.utils.moneyfmt`, but using the site settings
    :attr:`lino.Lino.decimal_group_separator`
    and
    :attr:`lino.Lino.decimal_separator`.
    """
    kw.setdefault('sep',settings.SITE.decimal_group_separator)
    kw.setdefault('dp',settings.SITE.decimal_separator)
    return moneyfmt(v,places=places,**kw)



try:
    import ho.pisa as pisa
    #pisa.showLogging()
except ImportError:
    pisa = None

#~ try:
    #~ import appy
#~ except ImportError:
    #~ appy = None
    
try:
    import pyratemp
except ImportError:
    pyratemp = None
        
#~ def filename_root(elem):
    #~ return elem._meta.app_label + '.' + elem.__class__.__name__

def model_group(model):
    return model._meta.app_label + '/' + model.__name__



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
        #~ self.old_templates_dir = os.path.join(settings.SITE.webdav_root,'doctemplates',self.templates_name)
        #~ self.templates_url = settings.SITE.webdav_url + '/'.join(('doctemplates',self.templates_name))
        

            
    def __unicode__(self):
        return unicode(self.label)
        
    def get_target(self,action,elem):
        "used by `get_target_name`"
        return MediaFile(self.use_webdav,self.cache_name, self.name, elem.filename_root() + self.target_ext)
        
        
    def get_target_name(self,action,elem):
        return self.get_target(action,elem).name
    def get_target_url(self,action,elem):
        return self.get_target(action,elem).url
        
    #~ def get_target_parts(self,action,elem):
        #~ "used by `get_target_name`"
        #~ return [self.cache_name, self.name, elem.filename_root() + self.target_ext]
        #~ 
    #~ def get_target_name(self,action,elem):
        #~ "return the output filename to generate on the server"
        #~ if self.use_webdav and settings.SITE.use_davlink:
            #~ return os.path.join(settings.SITE.webdav_root,*self.get_target_parts(action,elem))
        #~ return os.path.join(settings.MEDIA_ROOT,*self.get_target_parts(action,elem))
        #~ 
    #~ def get_target_url(self,action,elem):
        #~ "return the url that points to the generated filename on the server"
        #~ if self.use_webdav and settings.SITE.use_davlink:
            #~ return settings.SITE.webdav_url + "/".join(self.get_target_parts(action,elem))
        #~ return settings.SITE.build_media_url(*self.get_target_parts(action,elem))
            
    def build(self,ar,action,elem):
        raise NotImplementedError
        
    #~ def get_template_url(self,action,elem):
        #~ raise NotImplementedError
        
class DjangoBuildMethod(BuildMethod):
    """
    Using Django's templating engine.
    """
    def get_template(self,action,elem):
        tpls = action.get_print_templates(self,elem)
        if len(tpls) == 0:
            raise Warning("No templates defined for %r" % elem)
        #~ logger.debug('make_pisa_html %s',tpls)
        try:
            return select_template(tpls)
        except TemplateDoesNotExist,e:
            raise Warning("No template found for %s (%s)" % (e,tpls))

    def render_template(self,elem,tpl,**context): # ,MEDIA_URL=settings.MEDIA_URL):
        context.update(
          instance=elem,
          title = unicode(elem),
          MEDIA_URL = settings.MEDIA_ROOT.replace('\\','/') + '/',
        )
        return tpl.render(Context(context))
        
class PisaBuildMethod(DjangoBuildMethod):
    """
    Generates .pdf files from .html templates.
    Usage example see :ref:`lino.tutorials.pisa`.
    """
    name = 'pisa'
    target_ext = '.pdf'
    #~ button_label = _("PDF")
    template_ext = '.pisa.html'  
    
    def build(self,ar,action,elem):
        tpl = self.get_template(action,elem) 
        filename = action.before_build(self,elem)
        if filename is None:
            return
        #~ html = self.render_template(elem,tpl,request=ar.request)
        html = self.render_template(elem,tpl,ar=ar)
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
  
    def get_template_leaf(self,action,elem):
      
        tpls = action.get_print_templates(self,elem)
        #~ if not tpls:
            #~ return
        if len(tpls) != 1:
            raise Exception(
              "%s.get_print_templates() must return exactly 1 template (got %r)" % (
                elem.__class__.__name__,tpls))
        tpl_leaf = tpls[0]
        lang = elem.get_print_language()
        if lang != settings.SITE.DEFAULT_LANGUAGE.django_code:
            name = tpl_leaf[:-len(self.template_ext)] + "_" + lang + self.template_ext
            from lino.utils.config import find_config_file
            #~ if find_config_file(name,self.get_group(elem)):
            if find_config_file(name,elem.get_templates_group()):
                return name
        return tpl_leaf
            #~ tplfile = os.path.normpath(os.path.join(self.templates_dir,lang,tpl_leaf))
            #~ if not os.path.exists(tplfile):
                #~ lang = babel.DEFAULT_LANGUAGE
        #~ return lang + '/' + tpl_leaf
        
    #~ def get_template_url(self,action,elem):
        #~ tpl = self.get_template_leaf(action,elem)
        #~ return self.templates_url + '/' + tpl
        
    def get_template_file(self,ar,action,elem):
        from lino.utils.config import find_config_file
        tpl_leaf = self.get_template_leaf(action,elem)
        tg = elem.get_templates_group()
        tplfile = find_config_file(tpl_leaf,tg)
        if not tplfile:
            raise Warning("No file %s/%s" % (tg,tpl_leaf))
        #~ tplfile = os.path.normpath(os.path.join(self.templates_dir,tpl_leaf))
        return tplfile
        
    def build(self,ar,action,elem):
        #~ if elem is None:
            #~ return
        target = action.before_build(self,elem)
        if not target:
            return
        tplfile = self.get_template_file(ar,action,elem)
        return self.simple_build(ar,elem,tplfile,target)
        
    def simple_build(self,ar,elem,tpl,target):
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
    
    def simple_build(self,ar,elem,tpl,target):
        #~ from lino.models import get_site_config
        #~ from appy.pod.renderer import Renderer
        #~ renderer = None
        """
        When the source string contains non-ascii characters, then 
        we must convert it to a unicode string.
        """
        lang = str(elem.get_print_language())
        #~ savelang = dbutils.get_language()
        #~ dbutils.set_language(lang)
        logger.info(u"appy.pod render %s -> %s (language=%r,params=%s",
            tpl,target,lang,settings.SITE.appy_params)
        def f():
            context = elem.get_printable_context(ar)
            context.update(self=elem)
            Renderer(ar,tpl, context, target,**settings.SITE.appy_params).run()
        dbutils.run_with_language(lang,f)
        #~ dbutils.set_language(savelang)
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
    
    def simple_build(self,ar,elem,tpl,target):
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
    
    def simple_build(self,ar,elem,tpl,target):
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

    
    
def get_build_method(elem):
    bmname = elem.get_build_method()
    if not bmname:
        raise Exception("%s has no build method" % elem)
    bm = bm_dict.get(bmname,None)
    if bm is None:
        raise Exception("Build method %r doesn't exist. Requested by %r." % (bmname,elem))
    return bm
    
    
#~ class PrintTableAction(actions.TableAction):
    #~ def run_from_ui(self,ar,**kw):
        #~ bm = get_build_method(elem)
        #~ url = bm.get_target_url(self,elem)
        #~ kw.update(open_url=url)
        #~ return ar.ui.success_response(**kw)
  
    
        

#~ class PrintAction(actions.RedirectAction):
class BasePrintAction(actions.Action):
    """
    Base class for all "Print" actions.
    """
    sort_index = 50
    url_action_name = 'print'
    label = _('Print')
    
    
    def attach_to_actor(self,actor,name):
        if not dbutils.resolve_app('system'):
            return False
        return super(BasePrintAction,self).attach_to_actor(actor,name)
    
    def is_callable_from(self,caller):
        return isinstance(caller,(actions.GridEdit, 
            actions.ShowDetailAction,
            actions.ShowEmptyTable)) # but not from InsertRow
    
    #~ def __init__(self,rpt,*args,**kw):
        #~ self.actor = rpt
        #~ actions.Action.__init__(self,*args,**kw)
    
    def get_print_templates(self,bm,elem):
        return elem.get_print_templates(bm,self)
        
    def before_build(self,bm,elem):
        """Return the target filename if a document needs to be built,
        otherwise return ``None``.
        """
        elem.before_printable_build(bm)
        filename = bm.get_target_name(self,elem)
        if not filename:
            return
        if os.path.exists(filename):
            logger.debug(u"%s %s -> overwrite existing %s.",bm,elem,filename)
            os.remove(filename)
        else:
            #~ logger.info("20121221 makedirs_if_missing %s",os.path.dirname(filename))
            settings.SITE.makedirs_if_missing(os.path.dirname(filename))
        logger.debug(u"%s : %s -> %s", bm,elem,filename)
        return filename
        
        
class CachedPrintAction(BasePrintAction):
    """
    Note that this action should rather be called 
    'Open a printable document' than 'Print'.
    For the user they are synonyms as long as 
    Lino doesn't support server-side printing.
    """
    select_rows = False
    http_method = 'POST'
    icon_name = 'printer'
    
    def before_build(self,bm,elem):
        if elem.build_time:
            return
        return BasePrintAction.before_build(self,bm,elem)
            
    def run_from_ui(self,ar,**kw):
        #~ obj = ar.selected_rows[0]        
        #~ assert obj is None
        if len(ar.selected_rows) == 1:
            obj = ar.selected_rows[0]
            bm = get_build_method(obj)
            mf = bm.get_target(self,obj)
            
            if obj.build_time is None:
                obj.build_target(ar)
                kw.update(message=_("%s printable has been built.") % obj)
            else:
                kw.update(message=_("Reused %s printable from cache.") % obj)
            kw.update(refresh=True)
            #~ kw.update(open_url=mf.url)
            if bm.use_webdav and settings.SITE.use_davlink and ar.request is not None:
                kw.update(open_davlink_url=ar.request.build_absolute_uri(mf.url))
            else:
                kw.update(open_url=mf.url)
            return ar.success(**kw)

        def ok():
            #~ qs = [ar.actor.get_row_by_pk(pk) for pk in ar.selected_pks]
            mf = self.print_multiple(ar,ar.selected_rows)
            kw.update(open_url=mf.url)
            #~ kw.update(refresh_all=True)
            return kw
        msg = _("This will print %d rows.") % len(ar.selected_pks)
        return ar.confirm(ok, msg, _("Are you sure?"))

    def print_multiple(self,ar,qs):
        pdfs = []
        for obj in qs:
            #~ assert isinstance(obj,CachedPrintable)
            #~ obj.register(ar) # moved call to register to Registrable.before_printable_build
            if obj.build_time is None:
                obj.build_target(ar)
            pdf = obj.get_target_name()
            assert pdf is not None
            pdfs.append(pdf)
                
        mf = TmpMediaFile(ar,'pdf')
        settings.SITE.makedirs_if_missing(os.path.dirname(mf.name))
        merge_pdfs(pdfs,mf.name)
        return mf


class EditTemplate(BasePrintAction):
    sort_index = 51
    url_action_name = 'edit_tpl'
    label = _('Edit Print Template')
    required = dict(user_level='manager')
    
    def run_from_ui(self,ar,**kw):
        elem = ar.selected_rows[0]
        bm = get_build_method(elem)
        tplfile = bm.get_template_file(ar,self,elem)
        kw.update(message=_("Template file: %s ") % tplfile)
        kw.update(alert=True)
        url = "file://" + tplfile
        if bm.use_webdav and settings.SITE.use_davlink:
            kw.update(open_davlink_url=ar.request.build_absolute_uri(url))
        else:
            kw.update(open_url=url)
        return ar.success(**kw)
    

      
class DirectPrintAction(BasePrintAction):
    """
    A Print Action that uses a hard-coded template and no cache.
    """
    url_action_name = None
    icon_name='printer'
    
    #~ def __init__(self,rpt,name,label,bmname,tplname):
    #~ def __init__(self,label=None,tplname='Default',build_method=None,**kw):
    def __init__(self,label=None,tplname=None,build_method=None,**kw):
        #~ if name is None: name = 'print'
        #~ if label is None: label = _("Print")
        #~ if tplname is None: tplname = 'Default'
        super(DirectPrintAction,self).__init__(label,**kw)
        #~ BasePrintAction.__init__(self,rpt,name,label)
        #~ self.bm =  bm_dict.get(build_method or settings.SITE.preferred_build_method)
        self.build_method = build_method
        self.tplname = tplname
        
    #~ def setup(self,actor,name):
        #~ self.url_action_name = name
        #~ super(DirectPrintAction,self).setup(actor,name)
        
    def get_print_templates(self,bm,elem):
        #~ assert bm is self.bm
        if self.tplname:
            return [ self.tplname + bm.template_ext ]
        return elem.get_print_templates(bm,self)
        #~ return super(DirectPrintAction,self).get_print_templates(bm,elem)
        
        
    def run_from_ui(self,ar,**kw):
        elem = ar.selected_rows[0]
        bm =  bm_dict.get(
            self.build_method or 
            settings.SITE.site_config.default_build_method)
        #~ if self.tplname:
            #~ if not self.tplname.endswith(bm.template_ext):
                #~ raise Exception("Invalid template for build method %r" % bm.name)
        bm.build(ar,self,elem)
        #~ target = settings.MEDIA_URL + "/".join(bm.get_target_parts(self,elem))
        #~ return rr.ui.success_response(open_url=target,**kw)
        url = bm.get_target_url(self,elem)
        if bm.use_webdav and settings.SITE.use_davlink:
            url = ar.request.build_absolute_uri(url)
            kw.update(open_davlink_url=url)
        else:
            kw.update(open_url=url)
        return ar.success(**kw)
    
#~ class EditTemplateAction(dd.Action):
    #~ name = 'tpledit'
    #~ label = _('Edit template')
    
    #~ def run_from_ui(self,rr,elem,**kw):
        #~ bm = get_build_method(elem)
        #~ target = bm.get_template_url(self,elem)
        #~ return rr.ui.success_response(open_url=target,**kw)
    
class ClearCacheAction(actions.Action):
    """
    Defines the :guilabel:`Clear cache` button on a Printable record.
    
    The `run_from_ui` method has an optional keyword argmuent
     `force`. This is set to True in `docs/tests/debts.rst` 
     to avoid compliations.
    
    """
    sort_index = 51
    url_action_name = 'clear'
    label = _('Clear cache')
    #~ debug_permissions = 20121127
    
    icon_name = 'printer_delete'
    
    #~ def disabled_for(self,obj,request):
        #~ if not obj.build_time:
            #~ return True
            
    def get_action_permission(self,ar,obj,state):
        # obj may be None when Lino asks whether this action 
        # should be visible in the UI
        if obj is not None and not obj.build_time:
            return False
        return super(ClearCacheAction,self).get_action_permission(ar,obj,state)
    
    def run_from_ui(self,ar):
        elem = ar.selected_rows[0]
        def doit():
            elem.clear_cache()
            return ar.success("%s printable cache has been cleared." % elem,refresh=True)
            
        t = elem.get_cache_mtime()
        if t is not None and t != elem.build_time:
            #~ logger.info("%r != %r", elem.get_cache_mtime(),elem.build_time)
            return ar.confirm(doit,
                _("This will discard all changes in the generated file."),
                _("Are you sure?"))
            #~ logger.info("Got confirmation to discard changes in %s", elem.get_target_name())
        #~ else:
            #~ logger.info("%r == %r : no confirmation", elem.get_cache_mtime(),elem.build_time)
        return doit()
        
    
    
class PrintableType(Model):
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
        """
        Note that `get_templates_group` is 
        a class method on `PrintableType`
        an instance method on `Printable`
        """
        #~ return cls.templates_group or cls._meta.app_label
        return cls.templates_group # or full_model_name(cls)
        
    @chooser(simple_values=True)
    def template_choices(cls,build_method):
        return cls.get_template_choices(build_method,cls.get_templates_group())
        
    @classmethod
    def get_template_choices(cls,build_method,template_group):
        if not build_method:
            build_method = settings.SITE.site_config.default_build_method 
        #~ return get_template_choices(cls,build_method)
        bm = bm_dict.get(build_method,None)
        if bm is None:
            raise Exception("%r : invalid print method name." % build_method)
        from lino.utils.config import find_template_config_files
        #~ return find_template_config_files(bm.template_ext,bm.get_group(elem))
        return find_template_config_files(bm.template_ext,template_group)
        
        
    
class BasePrintable(object):
    """
    Common base for :class:`Printable`.and :class:`CachedPrintable`.
    """
    def before_printable_build(self,bm):
        pass
        
    def get_print_language(self):
        return settings.SITE.DEFAULT_LANGUAGE.django_code
        
    def get_templates_group(self):
        return model_group(self.__class__)
        
    def filename_root(self):
        return self._meta.app_label + '.' + self.__class__.__name__ + '-' + str(self.pk)
        
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
        return settings.SITE.site_config.default_build_method
        #~ return settings.SITE.preferred_build_method 
        #~ return 'pisa'
        
    def get_printable_context(self,ar,**kw):
        """
        Defines the certain names of a template context.
        
        See :doc:`/user/templates_api`.
        
        :class:`lino.modlib.notes.models.Note` extends this.
        """
        def translate(s):
            return _(s.decode('utf8'))
        from lino import dd
        kw.update(this=self,
            dtos=dd.fds, # obsolete
            dtosl=dd.fdf, # obsolete
            dtomy=dtomy, # obsolete
            mtos=decfmt,
            fds=dd.fds,
            fdm=dd.fdm,
            fdl=dd.fdl,
            fdf=dd.fdf,
            fdmy=dd.fdmy,
            babelattr=dd.babelattr,
            babelitem=settings.SITE.babelitem,
            tr=settings.SITE.babelitem,
            iif=iif,
            settings=settings,
            ar=ar,
            site_config=settings.SITE.site_config,
            _ = translate,
            )
        kw.update(language=self.get_print_language())
        return kw
            
class Printable(BasePrintable):
    """
    Mixin for Models whose instances can "print" (generate a printable document).
    """
  
    do_print = DirectPrintAction() 
    edit_template = EditTemplate()
    
   
class CachedPrintable(Duplicable,BasePrintable):
    """
    Mixin for Models that generate a unique external file at a 
    determined place when being printed.
    
    Adds a "Print" button, a "Clear cache" button and a `build_time` 
    field.
    
    The "Print" button of a 
    :class:`CachedPrintable <lino.mixins.printable.CachedPrintable>`
    transparently handles the case when multiple rows are selected. 
    If multiple rows are selected (which is possible only when 
    :attr:`cell_edit <lino.core.tables.AbstractTable.cell_edit>` is True),
    then it will automatically:
    
    - build the cached printable for those objects who don't yet have 
      one
      
    - generate a single temporary pdf file which is a merge of these 
      individual cached printable docs
    
    
    """
    do_print = CachedPrintAction()
    do_clear_cache = ClearCacheAction()
    #~ print_all = PrintAll()
    
    #~ must_build = models.BooleanField(_("must build"),default=True,editable=False)
    build_time = models.DateTimeField(_("build time"),null=True,editable=False)
    """
    Timestamp of the built target file. Contains `None` 
    if no build hasn't been called yet.
    """
    
    
    
    class Meta:
        abstract = True
        
      
    #~ def print_from_posting(self,posting,ar,**kw):
        #~ return self.do_print.run_from_session(ar,**kw)
        
    def on_duplicate(self,ar,master):
        super(CachedPrintable,self).on_duplicate(ar,master)
        self.build_time = None
        
    def get_target_name(self):
        if self.build_time:
            return get_build_method(self).get_target_name(self.do_print,self)
        
    def get_target_url(self):
        return get_build_method(self).get_target_url(self.do_print,self)
        
    def get_cache_mtime(self):
        filename = self.get_target_name()
        if not filename: return None
        try:
            t = os.path.getmtime(filename)
        except OSError,e:
            return None
        return datetime.datetime.fromtimestamp(t)
        
    def clear_cache(self):
        #~ elem.must_build = True
        self.build_time = None
        self.save()
        
    def build_target(elem,ar):
        bm = get_build_method(elem)
        t = bm.build(ar,elem.__class__.do_print,elem)
        if t is None:
            raise Exception("%s : build() returned None?!")
        elem.build_time = datetime.datetime.fromtimestamp(t)
        elem.save()

class TypedPrintable(CachedPrintable):
    """
    A :class:`CachedPrintable` that uses a "Type" for deciding which template 
    to use on a given instance. 
    
    A TypedPrintable model must define itself a field `type` which is a ForeignKey 
    to a Model that implements :class:`PrintableType`.
    
    Alternatively you can override :meth:`get_printable_type` 
    if you want to name the field differently. An example of 
    this is :attr:`lino.modlib.sales.models.SalesDocument.imode`.
    """
    
    #~ type = NotImplementedError
    type = None
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
        return settings.SITE.site_config.default_build_method 
        
    def get_print_templates(self,bm,action):
        ptype = self.get_printable_type()
        if ptype is None:
            return super(TypedPrintable,self).get_print_templates(bm,action)
        tplname = ptype.template or bm.default_template
        if not tplname.endswith(bm.template_ext):
            raise Warning(
              "Invalid template '%s' configured for %s '%s' (expected filename ending with '%s')." %
              (tplname,ptype.__class__.__name__,unicode(ptype),bm.template_ext))
        return [ tplname ]
        #~ return [ ptype.get_templates_group() + '/' + ptype.template ]
        
    #~ def get_print_language(self,bm):
        #~ return self.language


