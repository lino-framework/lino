# -*- coding: UTF-8 -*-
## Copyright 2013 Luc Saffre
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
A  Sphinx extension used to write multilingual documentation for a 
Lino application.
"""

from __future__ import unicode_literals, print_function

from sphinx.ext.autodoc import ModuleLevelDocumenter
from sphinx.util.docstrings import prepare_docstring
from sphinx.util import force_decode
from sphinx.util.nodes import make_refnode


#~ from sphinx.config import Config
#~ from sphinx.errors import SphinxError, SphinxWarning, ExtensionError, \
     #~ VersionRequirementError
from sphinx.domains import ObjType
#~ from sphinx.domains.std import GenericObject, Target, StandardDomain
from sphinx.domains.std import StandardDomain
from sphinx.domains.python import PyModulelevel

from sphinx.roles import XRefRole
from sphinx.util import ws_re
from sphinx import addnodes

from docutils.parsers.rst import roles
from docutils import nodes, utils
from docutils.nodes import fully_normalize_name, whitespace_normalize_name


from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils import translation 
from django.utils.encoding import force_unicode

from lino import dd

from lino.core import actors
from lino.core import choicelists
from lino.core import dbtables
from atelier.utils import unindent
from atelier import rstgen
from djangosite.dbutils import full_model_name
#~ from djangosite.dbutils import set_language

from atelier.sphinxconf import Django2rstDirective


import lino.ui.urls # hack: trigger ui instantiation

from lino.core import actions    


#~ def refto(x):
    #~ if x is None: 
        #~ return '`None`'
    #~ if issubclass(x,models.Model):
        #~ return ':ref:`' + force_unicode(x._meta.verbose_name) + ' <' \
            #~ + settings.SITE.userdocs_prefix + full_model_name(x) + '>`'
    #~ return ':ref:`' + x.verbose_name + ' <' + settings.SITE.userdocs_prefix \
        #~ + full_model_name(x.model) + '.' + x.name + '>`'
        
#~ def actor_name(a): return settings.SITE.userdocs_prefix + str(a).lower()
def actor_name(a): 
    #~ return settings.SITE.userdocs_prefix + str(a).lower()
    return fully_normalize_name(settings.SITE.userdocs_prefix + str(a))
    #~ return settings.SITE.userdocs_prefix + str(a)
def model_name(m): return settings.SITE.userdocs_prefix + full_model_name(m).lower()
def app_name(a): 
    assert a.__name__.endswith('.models')
    parts = a.__name__.split('.')
    return settings.SITE.userdocs_prefix + parts[-2]
    #~ app = getattr(a,'App',None)
    #~ if app is None:
        #~ name = parts[-2]
    #~ else:
        #~ name = parts[-2]
    #~ raise Exception(a.__name__)
    #~ return settings.SITE.userdocs_prefix + name

def actor_ref(rpt,text=None):
    if text is None:
        text = force_unicode(rpt.label or rpt.title or str(rpt))
    return ':ddref:`%s <%s>`' % (text,rpt)

def model_ref(m,text=None):
    if text is None:
        text = force_unicode(m._meta.verbose_name)
    return ':ref:`%s <%s>`' % (text,model_name(m))

def rptlist(l):
    return ', '.join([actor_ref(a) for a in l])
    #~ return ', '.join([
        #~ ":ref:`%s (%s) <%s>`" % (str(rpt),force_unicode(rpt.label),actor_ref(rpt)) 
        #~ for rpt in l])

def typeref(cls):
    text = cls.__name__
    target = cls.__module__ + '.' + cls.__name__
    #~ return ":coderef:`%s <%s>`" % (text,target)
    return ":class:`%s <%s>`" % (text,target)
    
def old_fieldtype(f):
    if isinstance(f,models.ForeignKey):
        #~ return f.__class__.__name__ + " to " + refto(f.rel.to)
        return f.__class__.__name__ + " to " + model_ref(f.rel.to)
    return f.__class__.__name__

def fieldtype(f):
    s = typeref(f.__class__)
    if isinstance(f,models.ForeignKey):
        s = _("%(classref)s to %(model)s") % dict(classref=s,model=model_ref(f.rel.to))
        #~ print(20130908, s)
    if isinstance(f,choicelists.ChoiceListField):
        s = _("%(classref)s to %(model)s") % dict(classref=s,model=actor_ref(f.choicelist))
    return s


def fields_ul(fields):
    helpless = []
    def field2li(fld):
        s = "**%s**" % unicode(f.verbose_name).strip()
        s += " (``%s``, %s)" % (f.name,fieldtype(f))
        if f.help_text:
            s += " -- " + unicode(f.help_text)
            return s
        helpless.append(s)
        return None
        
    items = []
    for f in fields:
        if not hasattr(f,'_lino_babel_field'):
            s = field2li(f)
            if s:
                items.append(s)
    #~ items = [ field2li(f) for f in fields if not hasattr(f,'_lino_babel_field')]
    if len(helpless):
        s = ', '.join(helpless)
        if len(items):
            s = _("... and %s") % s
        items.append(s)
    return rstgen.ul(items)
    
def fields_table(fields):
    headers = ["name","type"]
    #~ formatters = [
      #~ lambda f: f.name,
      #~ lambda f: f.__class__.__name__,
    #~ ]
    headers.append("verbose name")
    headers.append("help text")
        
    def rowfmt(f):
        cells = [
          f.name,
          fieldtype(f),
          f.verbose_name,
          f.help_text
        ]
        #~ for lng in babel.AVAILABLE_LANGUAGES:
            #~ babel.set_language(lng)
            #~ cells.append(force_unicode(_(f.verbose_name)))
        #~ cells.append(f.help_text)
        return cells
    rows = [ rowfmt(f) for f in fields if not hasattr(f,'_lino_babel_field')]
    return rstgen.table(headers,rows)



def get_actor_description(self):
    """
    `self` is the actor
    """
    body = "\n\n"
    if self.help_text:
        body += unindent(force_unicode(self.help_text).strip()) + "\n\n"

    #~ ll = self.get_handle().list_layout
    #~ if ll is not None:
        #~ body += fields_table([ e.field for e in ll.main.columns] )
    
    #~ model_reports = [r for r in dbtables.master_reports if r.model is self.model]
    #~ if model_reports:
        #~ body += '\n\nMaster tables: %s\n\n' % rptlist(model_reports)
    #~ if getattr(model,'_lino_slaves',None):
        #~ body += '\n\nSlave tables: %s\n\n' % rptlist(model._lino_slaves.values())
    
    return body
      
#~ def get_model_description(self):
    #~ """
    #~ `self` is the actor
    #~ """
    #~ body = "\n\n"
    #~ help_text = getattr(self,'help_text',None)
    #~ if help_text:
        #~ body += unindent(force_unicode(help_text).strip()) + "\n\n"
#~ 
    #~ body += fields_table(self._meta.fields)
    #~ 
    #~ return body
    
#~ from atelier.sphinxconf import srcref    
    
IGNORED_ACTIONS = (actions.GridEdit,actions.SubmitDetail,
    actions.ShowDetailAction,
    actions.DeleteSelected,
    actions.InsertRow,actions.SubmitInsert)
    
def menuselection(mi):
    s = my_escape(unicode(mi.label).strip())
    p = mi.parent
    while p is not None:
        if p.label:
            s = my_escape(unicode(p.label).strip()) + " --> " + s
        p = p.parent
    return ":menuselection:`%s`" % s
      
def actions_ul(action_list):
    items = []
    for ba in action_list:
        label = ba.action.label
        desc = "**%s** (" % unicode(label).strip()
        if ba.action.action_name:
            desc += "``%s``" % ba.action.action_name
            
        desc += ", %s)" % typeref(ba.action.__class__)
        if ba.action.help_text:
            desc += " -- " + unicode(ba.action.help_text)
        items.append(desc)
    return rstgen.ul(items)
    
from lino.core.menus import find_menu_item

def my_escape(s):
    s = s.replace("\u25b6","")
    return s
    
def actors_overview_ul(model_reports):
    items = []
    for tb in model_reports:
        desc = actor_ref(tb)
        #~ label = unicode(tb.title or tb.label)
        #~ desc += " (%s)" % str(tb)
        desc += " (%s)" % typeref(tb)
        mi = find_menu_item(tb.default_action)
        if mi is not None:
            desc += _(" (Menu %s)") % menuselection(mi)
            #~ print(unicode(mi.label).strip())
        if tb.help_text:
            desc += " -- " + unicode(tb.help_text).strip()

        items.append(desc)
    return rstgen.ul(items)

class ActorsOverviewDirective(Django2rstDirective):
    def get_rst(self):
        lng = self.state.document.settings.env.config.language
        with translation.override(lng):
            #~ set_language(lng)
            actor_names = ' '.join(self.content).split()
            items = []
            for an in actor_names:
                cls = settings.SITE.modules.resolve(an)
                if not isinstance(cls,type):
                    raise Exception("%s is not an actor." % self.content[0])
                items.append("%s : %s" % (actor_ref(cls),cls.help_text or ''))
            return rstgen.ul(items)
            
def resolve_name(name):
    l = name.split('.')
    if len(l) == 1:
        return 1, dd.resolve_app(name)
    if len(l) == 3:
        model = settings.SITE.modules.resolve(l[0]+'.'+l[1])
        return 3, model.get_data_elem(l[2])
    return len(l), settings.SITE.modules.resolve(name)
    
def form_lines():
    yield '<script >'
    
class FormDirective(Django2rstDirective):
    def get_rst(self):
        level, cls = resolve_name(self.content[0])
        s = ''
        with translation.override(self.state.document.settings.env.config.language):
            s = '\n'.join(list(form_lines()))
        return s
    
class ActorDirective(Django2rstDirective):
    #~ has_content = False
    titles_allowed = True
    #~ debug = True
    def get_rst(self):
        #~ from actordoc import get_actor_description
        #~ from django.conf import settings
        #~ from djangosite.dbutils import set_language
        with translation.override(self.state.document.settings.env.config.language):
        #~ lng = self.state.document.settings.env.config.language
        #~ set_language(lng)
            level, cls = resolve_name(self.content[0])
            if isinstance(cls,models.Field):
                fld = cls
                s = ''
                name = str(fld.model)+'.'+fld.name
                title = force_unicode(fld.verbose_name).strip()
                s += "\n.. index::\n   single: " 
                s += unicode(_('%s (field in "%s")') % (title,fld.model))
                s += '\n\n'
                s += rstgen.header(level,_("The **%s** field") % title)
                if len(self.content) > 1:
                    s += '\n'.join(self.content[1:])
                    s += '\n\n'
                return s
                
            if isinstance(cls,dd.__class__): # it's a module (an app)
                s = ''
                name = app_name(cls)
                app = getattr(cls,'App',None)
                if app is None:
                    title = name
                else:
                    title = unicode(app.verbose_name)
                
                s += "\n.. index::\n   single: " 
                s += unicode(_('%s (app)') % title)
                s += '\n\n.. _'+ name + ':\n'
                s += '\n'
                s += rstgen.header(level,_("The %s app") % title)
                return s
                
            if not isinstance(cls,type):
                raise Exception("%s is not an actor." % self.content[0])
                
            if issubclass(cls,models.Model):
                model = cls
                #~ if full_model_name(cls) == 'newcomers.Broker':
                    #~ self.debug = True
                #~ self.add_model_index_entry(cls)
                
                s = ''
                name = model_name(model).lower()
                title = force_unicode(model._meta.verbose_name)
                s += "\n.. index::\n   single: " 
                s += unicode(_('%s (model in app "%s")') % (title,model._meta.app_label))
                s += '\n\n'
                
                #~ title = unicode(cls._meta.verbose_name)
                #~ indextext = _('%s (%s)') % (full_model_name(cls),title)
                #~ name = model_name(cls)
                #~ self.index_entries.append(('single', indextext, name, ''))
                #~ self.add_ref_target(name,name)
                s += '\n\n.. _'+ name + ':\n'
                
                s += '\n'
                s += rstgen.header(level,_("The %s model") % title)
                #~ print(s)
                #~ s += rstgen.header(3,_('%s (%s)') % (title,full_model_name(cls)))
                s += '\n'
                s += '\n:Internal name: ``%s``\n' % full_model_name(cls)
                s += '\n:Implemented by: %s\n' % typeref(cls)
                s += '\n'
                
                if len(self.content) > 1:
                    s += '\n'.join(self.content[1:])
                    s += '\n\n'
                    
                model_reports = [r for r in dbtables.master_reports if r.model is cls]
                model_reports += [r for r in dbtables.slave_reports if r.model is cls]
                #~ s += rstgen.boldheader(_("Tables on a %s") % cls._meta.verbose_name)
                s += rstgen.boldheader(_("Views on %s") % cls._meta.verbose_name)
                s += actors_overview_ul(model_reports)
                    
                s += rstgen.boldheader(_("Fields in %s") % cls._meta.verbose_name)
                s += fields_ul(cls._meta.fields)
                
                action_list = cls._lino_default_table.get_actions()
                #~ action_list = [ba for ba in action_list if ba.action.sort_index >= 30]
                action_list = [ba for ba in action_list if not isinstance(ba.action,IGNORED_ACTIONS)]
                if action_list:
                    s += '\n'
                    s += rstgen.boldheader(_("Actions on %s") % cls._meta.verbose_name)
                    s += actions_ul(action_list)
                    
                slave_tables = getattr(cls,'_lino_slaves',{}).values()
                if slave_tables:
                    s += rstgen.boldheader(_("Tables referring to %s") % cls._meta.verbose_name)
                    #~ for tb in slave_tables:
                        #~ s += '\n.. _'+ settings.SITE.userdocs_prefix + str(tb) + ':\n'
                    #~ s += '\n'
                    #~ s += rstgen.header(4,_("Slave tables of %s") % cls._meta.verbose_name)
                    
                    #~ s += "\n\n**%s**\n\n" % _("Tables referring to %s") % cls._meta.verbose_name
                    s += actors_overview_ul(slave_tables)
                    
                
                #~ if model_reports:
                    #~ s += '\nMaster tables: %s\n' % rptlist(model_reports)
                #~ if slave_tables:
                    #~ s += '\nSlave tables: %s\n' % rptlist(slave_tables)
    
                return s
                
            if issubclass(cls,actors.Actor):
              
                title = force_unicode(cls.label or cls.title)
                indextext = _('%s (table in module %s)') % (title,cls.app_label)
                name = actor_name(cls)
                #~ if name == 'welfare.reception.waitingvisitors':
                    #~ self.debug = True
                #~ print(20130907, name)
                self.index_entries.append(('single', indextext, name, ''))
                #~ self.add_ref_target(name,name)
                
                s = ''
                s += '\n\n.. _%s:\n\n' % name
                s += rstgen.header(level,_("The %s view") % title)
                s += '\n:Internal name: ``%s`` (%s)\n' % (cls,typeref(cls))
                
                if len(self.content) > 1:
                    s += '\n'.join(self.content[1:])
                    s += '\n\n'
                
                s += '\n\n'
                s += get_actor_description(cls)
                s += '\n\n'
                return s
            raise Exception("Cannot handle actor %r." % cls)
            
    
    def run(self):
        self.index_entries = []
        #~ index_entries is a list of 4-tuples of 
        #~ ``(entrytype, entryname, target, ignored)``
        content = super(ActorDirective,self).run()
        indexnode = addnodes.index(entries=self.index_entries)
        return [indexnode] + content
        
        

    
class ddrefRole(XRefRole):
    
    nodeclass = addnodes.pending_xref
    innernodeclass = nodes.emphasis
    
    def __call__(self, typ, rawtext, text, lineno, inliner,
                 options={}, content=[]):
        #~ print('20130901',typ, rawtext, text, lineno, inliner,options, content)
        typ = 'std:ref'
        return XRefRole.__call__(self, typ, rawtext, text, lineno, 
            inliner, options, content)
                     
    def process_link(self, env, refnode, has_explicit_title, title, target):
        """Called after parsing title and target text, and creating the
        reference node (given in *refnode*).  This method can alter the
        reference node and must return a new (or the same) ``(title, target)``
        tuple.
        """
        
        #~ print(20130901, refnode, has_explicit_title, title, target)
        #~ 20130901 <pending_xref refdomain="" refexplicit="False" reftype="ddref"/> False cal.Event cal.Event
        
        target = ws_re.sub(' ', target) # replace newlines or tabs by spaces
        #~ target = ' '.join(target.split()) # replace newlines or tabs by spaces
        
        level, x = resolve_name(target)
        #~ x = settings.SITE.modules.resolve(target)
        if x is None:
            raise Exception("Could not resolve name %r" % target)
            
        with translation.override(env.config.language):
            if isinstance(x,models.Field):
                text = utils.unescape(unicode(x.verbose_name))
                target = model_name(x.model)+'.'+x.name
                print(target)
            elif isinstance(x,dd.__class__): # it's a module (an app)                
                text = utils.unescape(unicode(x.App.verbose_name))
                #~ target = model_name(x)
                target = settings.SITE.userdocs_prefix + target
                
            elif isinstance(x,type) and issubclass(x,models.Model):
                text = utils.unescape(unicode(x._meta.verbose_name))
                target = model_name(x)
            elif isinstance(x,type) and issubclass(x,actors.Actor):
                text = utils.unescape(unicode(x.title or x.label))
                target = actor_name(x)
            else:
                raise Exception("Don't know how to handle %r" % x)
        
        if not has_explicit_title:
            refnode['refexplicit'] = True # avoid replacing title by the heading text
            title = text
            
        refnode['refwarn'] = False # never warn
        
        #~ refnode['reftype'] = 'ref'
        
        #~ title = "[%s]" % title
        #~ if target == 'welfare.reception.waitingvisitors':
        #~ print("20130907 ddref to %s : title=%r" % (target,title))
        
        
        return title, target


def setup(app):
    
    app.add_directive('form', FormDirective)
    app.add_directive('actor', ActorDirective)
    app.add_directive('actors_overview', ActorsOverviewDirective)
    app.add_role('ddref', ddrefRole())
