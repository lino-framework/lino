## Copyright 2009-2012 Luc Saffre
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
Defines some system models, especially the :class:`SiteConfig` model.
Expected to be installed in every Lino application.
"""

import logging
logger = logging.getLogger(__name__)
#~ from lino.utils import dblogger

import cgi

from django.conf import settings
#~ from django.contrib.auth import models as auth
#~ from django.contrib.sessions import models as sessions
from django.contrib.contenttypes import models as contenttypes
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode 


#~ from django import forms
from django.db import models
from django.utils.translation import ugettext_lazy as _

#~ import lino
from lino import mixins
from lino import dd
#~ from lino import commands
from lino.mixins import printable
from lino.utils import babel
#~ from lino import choices_method, simple_choices_method
from lino.core.modeltools import obj2str, sorted_models_list, full_model_name
from lino.core.modeltools import resolve_field, UnresolvedModel
from lino.utils.choosers import chooser, get_for_field
from lino.utils.restify import restify
from lino.core import actions
from lino.core import changes
from lino.utils.xmlgen import html as xghtml

#~ from lino.core.changes import Change, Changes, ChangesByObject


#~ class BuildLinoJS(dd.RowAction):
class BuildSiteCache(dd.RowAction):
    """
    Rebuild the site cache.
    This action is available on :class:`About`.
    """
    label = _("Rebuild site cache")
    url_action_name = "buildjs"
    def run(self,elem,rr):
        rr.confirm(_("Are you sure?"))
        #~ rr.confirm(_("Are you really sure?"))
        rr.ui.build_site_cache(True)
        return rr.ui.success_response(
            """\
Seems that it worked. Refresh your browser. 
<br>
Note that other users might experience side effects because 
of the unexpected .js update, but there are no known problems so far.
Please report any anomalies.""",
            alert=_("Success"))

    


    
class SiteConfig(dd.Model):
    """
    This model should have exactly one instance, 
    used to store persistent global site parameters.
    Application code sees this as ``settings.LINO.config``.
    """
        
    default_build_method = models.CharField(max_length=20,
      verbose_name=_("Default build method"),
      default='appyodt',
      choices=printable.build_method_choices(),blank=True)
        
    def save(self,*args,**kw):
        super(SiteConfig,self).save(*args,**kw)
        settings.LINO.on_site_config_saved(self)
   
    def __unicode__(self):
        return force_unicode(_("Site Parameters"))

#~ class SiteConfigDetail(dd.FormLayout):
    #~ about = """
    #~ versions:40x5 startup_time:30
    #~ lino.ModelsBySite:70x10
    #~ """
    #~ config = """
    #~ default_build_method
    #~ """
    #~ main = "about config"
    
    #~ def setup_handle(self,lh):
        #~ lh.config.label = _("Site Parameters")
        #~ lh.about.label = _("About")
    
class SiteConfigs(dd.Table):
    """
    The table used to present the :class:`SiteConfig` row in a Detail form.
    See also :meth:`lino.Lino.get_site_config`.
    Deserves more documentation.
    """
    default_action = actions.ShowDetailAction()
    model = SiteConfig
    required = dict(user_level='manager')
    #~ default_action_class = dd.OpenDetailAction
    #~ has_navigator = False
    hide_top_toolbar = True
    #~ can_delete = perms.never
    detail_layout = """
    default_build_method
    # lino.ModelsBySite
    """
        
    do_build = BuildSiteCache()
    

if settings.LINO.is_installed('contenttypes'):

  class ContentTypes(dd.Table):
      """
      Deserves more documentation.
      """
      model = contenttypes.ContentType
      
      detail_layout = """
      id name app_label model base_classes
      lino.HelpTextsByModel
      """
      
      @dd.displayfield(_("Base classes"))
      def base_classes(self,obj,ar):
          chunks = []
          def add(cl):
              for b in cl.__bases__:
                  add(b)
              if issubclass(cl,dd.Model) and cl is not dd.Model and cl._meta.managed: # :
                  if getattr(cl,'_meta',False) and not cl._meta.abstract:
                      #~ logger.info("20120205 adding(%r)",cl)
                      ct = contenttypes.ContentType.objects.get_for_model(cl)
                      #~ chunks.append(ar.ui.ext_renderer.href_to(ct,unicode(cl._meta.verbose_name)))
                      chunks.append(ar.href_to(ct,unicode(cl._meta.verbose_name)))
          if obj is not None:
              #~ add(obj.model_class())
              for b in obj.model_class().__bases__:
                  add(b)
          return ', '.join(chunks)
      
      
      
  class HelpText(dd.Model):
      
      class Meta:
          verbose_name = _("Help Text")
          verbose_name_plural = _("Help Texts")
          
      content_type = models.ForeignKey(contenttypes.ContentType,
          verbose_name=_("Model"))
      field = models.CharField(_("Field"),max_length=200)

      help_text = dd.RichTextField(_("HelpText"),
          blank=True,null=True,format='plain')
      
      def __unicode__(self):
          return self.content_type.app_label + '.' + self.content_type.model + '.' + self.field
          #~ return self.content_type.app_label + '.' + self.content_type.name + '.' + self.field
          
      @chooser(simple_values=True)
      def field_choices(cls,content_type):
          l = []
          if content_type is not None:
              model = content_type.model_class()
              meta = model._meta
              #~ for f in meta.fields: yield f.name
              #~ for f in meta.many_to_many: yield f.name
              #~ for f in meta.virtual_fields: yield f.name
              for f in meta.fields: 
                  if not getattr(f,'_lino_babel_field',False):
                      l.append(f.name)
              for f in meta.many_to_many: l.append(f.name)
              for f in meta.virtual_fields: l.append(f.name)
              for a in model._lino_default_table.get_actions():
                  l.append(a.action_name)
              l.sort()
          return l
          
      #~ def get_field_display(cls,fld):
          #~ return fld

      @dd.virtualfield(models.CharField(_("Verbose name"),max_length=200))
      def verbose_name(self,request):
          #~ return unicode(self)
          #~ m = dd.resolve_model(self.content_type.app_label + '.' + self.content_type.name)
          m = self.content_type.model_class()
          #~ if isinstance(m,UnresolvedModel):
              #~ return str(m)
          de = m._lino_default_table.get_data_elem(self.field)
          if isinstance(de,models.Field):
              #~ return unicode(de.verbose_name)
              return "%s (%s)" % (unicode(de.verbose_name), unicode(_("database field")))
          if isinstance(de,dd.VirtualField):
              return unicode(de.return_type.verbose_name)
          if isinstance(de,actions.Action):
              return unicode(de.label)
          return str(de)
          #~ return unicode(resolve_field(unicode(self)).verbose_name)
              
              
              
  class HelpTexts(dd.Table):
      model = HelpText
      column_names = "field verbose_name help_text id content_type"
      
  class HelpTextsByModel(HelpTexts):
      master_key = 'content_type'
      


#~ if settings.LINO.is_installed('users'):
if settings.LINO.user_model:

    class TextFieldTemplate(mixins.AutoUser):
        """A reusable block of text that can be selected from a text editor to be 
        inserted into the text being edited.
        """
      
        class Meta:
            verbose_name = _("Text Field Template")
            verbose_name_plural = _("Text Field Templates")
            
        name = models.CharField(_("Designation"),max_length=200)
        description = dd.RichTextField(_("Description"),
            blank=True,null=True,format='html')
        text = dd.RichTextField(_("Template Text"),
            blank=True,null=True,format='html')
        
        def __unicode__(self):
            return self.name
            
    class TextFieldTemplates(dd.Table):
        detail_layout = """
        id name user
        description
        text
        """
        model = TextFieldTemplate
        required = dict(user_groups='office')

    class MyTextFieldTemplates(TextFieldTemplates,mixins.ByUser):
        pass
        

class Change(dd.Model):
    """
    Each `save()` of a watched object will generate one Change record.
    """
    class Meta:
        verbose_name = _("Change")
        verbose_name_plural = _("Changes")
            
    time = models.DateTimeField()
    type = changes.ChangeTypes.field()
    if settings.LINO.user_model:
        user = dd.ForeignKey(settings.LINO.user_model)
        
    object_type = models.ForeignKey(ContentType,related_name='changes_by_object')
    object_id = dd.GenericForeignKeyIdField(object_type)
    object = dd.GenericForeignKey('object_type','object_id',_("Object"))
    
    master_type = models.ForeignKey(ContentType,related_name='changes_by_master')
    master_id = dd.GenericForeignKeyIdField(master_type)
    master = dd.GenericForeignKey('master_type','master_id',_("Master"))
    
    #~ summary = models.CharField(_("Summary"),max_length=200,blank=True)
    #~ description = dd.RichTextField(format='plain')
    diff = dd.RichTextField(_("Changes"),format='plain',blank=True)
    
    def __unicode__(self):
        #~ return "#%s - %s" % (self.id,self.time)
        return "#%s" % self.id
    
class Changes(dd.Table):
    editable = False
    model = Change
    order_by = ['-time']
    detail_layout = """
    time user type master object id
    diff
    """
    
#~ class ChangesByObject(Changes):
class ChangesByMaster(Changes):
    """
    Slave Table showing the changes related to the current object
    """
    column_names = 'time user type object diff object_type object_id'
    master_key = 'master'




class Home(mixins.EmptyTable):
    """
    This is the "home page" or "welcome screen", the window to be displayed 
    when no other window is opened.
    """
    #~ debug_actions = True
    label = _("Home") 
    hide_window_title = True
    hide_top_toolbar = True
    #~ detail_layout = HomeDetail()
    detail_layout = """
    quick_links:80x1
    welcome
    """
    
    #~ @classmethod
    #~ def setup_actions(self):
        #~ "Overrides the default method. Home page needs no print method."
        #~ pass
        
    #~ @dd.virtualfield(dd.HtmlBox())
    #~ def tasks_summary(cls,self,req):
        #~ return cal.tasks_summary(req.ui,req.get_user())
    
    @dd.virtualfield(dd.HtmlBox())
    def quick_links(cls,self,req):
        quicklinks = settings.LINO.get_quicklinks(self,req.get_user())
        if quicklinks.items:
            chunks = []
            for mi in quicklinks.items:
                chunks.append(' ')
                chunks.append(req.ui.ext_renderer.window_action_button(
                  req,mi.bound_action))
            return xghtml.E.p('Quick Links:',*chunks)
      
    #~ @dd.virtualfield(dd.HtmlBox())
    #~ def missed_reminders(cls,self,req):
        #~ return cal.reminders(req.ui,req.get_user(),days_back=90,
          #~ max_items=10,before='<ul><li>',separator='</li><li>',after="</li></ul>")
          
    #~ @dd.constant('')
    #~ @dd.constant()
    #~ def welcome(cls,ui):
        #~ return "Welcome to the <b>%s</b> server." % cgi.escape(settings.LINO.title)
        
    @dd.virtualfield(dd.HtmlBox(_('Welcome')))
    def welcome(cls,self,ar):
        #~ MAXITEMS = 2
        u = ar.get_user()
        story = []
        
        if u.authenticated:
          
            intro = [_("Hi, "),u.first_name,'! ']
            story.append(xghtml.E.p(*intro))
            warnings = []
            
            #~ for T in (MySuggestedCoachings,cal.MyTasksToDo):
            for table,text in settings.LINO.get_todo_tables(ar):
                r = table.request(user=u)
                #~ r = T.request(subst_user=u)
                #~ r = ar.spawn(T)
                if r.get_total_count() != 0:
                    #~ for obj in r.data_iterator[-MAXITEMS]:
                        #~ chunks = [obj.summary_row(ar)]
                        #~ sep = ' : '
                        #~ for a in T.get_workflow_actions(ar,obj):
                            #~ chunks.append(sep)
                            #~ chunks.append(ar.row_action_button(obj,a))
                            #~ sep = ', '
                    
                    warnings.append(xghtml.E.li(
                        ar.href_to_request(r,text % r.get_total_count())))
                        #~ _("You have %d entries in ") % r.get_total_count(),
                        #~ ar.href_to_request(r,label)))
            
            #~ warnings.append(xghtml.E.li("Test 1"))
            #~ warnings.append(xghtml.E.li("Second test"))
            if len(warnings):
                #~ story.append(xghtml.E.h3(_("Warnings")))
                story.append(xghtml.E.h3(_("You have")))
                story.append(xghtml.E.ul(*warnings))
            else:
                story.append(xghtml.E.p(_("Congratulatons: you have no warnings.")))
        else:
            #~ story.append(xghtml.E.p("Please log in"))
            story.append(settings.LINO.get_guest_greeting())
        
        return xghtml.E.div(*story,class_="htmlText",style="margin:5px")
        

        
    
    #~ @dd.virtualfield(dd.HtmlBox(_('Missed reminders')))
    #~ def missed_reminders(cls,self,req):
        #~ return cal.reminders(req.ui,req.get_user(),days_back=90,
          #~ max_items=10,before='<ul><li>',separator='</li><li>',after="</li></ul>")

    #~ @dd.virtualfield(dd.HtmlBox(_('Upcoming reminders')))
    #~ def coming_reminders(cls,self,req):
        #~ return cal.reminders(req.ui,req.get_user(),days_forward=30,
            #~ max_items=10,before='<ul><li>',separator='</li><li>',after="</li></ul>")







SYSTEM_USER_LABEL = _("System")
OFFICE_MODULE_LABEL = _("Office")
  
def setup_main_menu(site,ui,user,m): 
    #~ office = m.add_menu("office",OFFICE_MODULE_LABEL)
    #~ office.add_action(MyTextFieldTemplates)
    pass

def setup_my_menu(site,ui,user,m): pass
  
def setup_config_menu(site,ui,user,m):
    office = m.add_menu("office",OFFICE_MODULE_LABEL)
    system = m.add_menu("system",SYSTEM_USER_LABEL)
    #~ m.add_action('links.LinkTypes')
    if site.user_model:
        system.add_action(site.user_model)
        office.add_action(MyTextFieldTemplates)
    #~ m.add_action(site.modules.users.Users)
    if site.is_installed('contenttypes'):
        system.add_action(site.modules.lino.ContentTypes)
        system.add_action(site.modules.lino.HelpTexts)
        #~ m.add_action(site.modules.lino.Workflows)
    #~ if site.use_tinymce:
    system.add_instance_action(site.site_config)
        
  
def setup_explorer_menu(site,ui,user,m):
    office = m.add_menu("office",OFFICE_MODULE_LABEL)
    system = m.add_menu("system",SYSTEM_USER_LABEL)
    if site.user_model:
        system.add_action(site.modules.users.Authorities)
        system.add_action(dd.UserGroups)
        system.add_action(dd.UserLevels)
        system.add_action(dd.UserProfiles)
    system.add_action(Changes)
    office.add_action(TextFieldTemplates)
  

dd.add_user_group('office',OFFICE_MODULE_LABEL)
