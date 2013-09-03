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



from lino.core import actors
from lino.core import choicelists
from lino.core import dbtables
from atelier.utils import unindent
from atelier import rstgen
from djangosite.dbutils import full_model_name
#~ from djangosite.dbutils import set_language

from atelier.sphinxconf import Django2rstDirective


import lino.ui.urls # hack: trigger ui instantiation


#~ def refto(x):
    #~ if x is None: 
        #~ return '`None`'
    #~ if issubclass(x,models.Model):
        #~ return ':ref:`' + force_unicode(x._meta.verbose_name) + ' <' \
            #~ + settings.SITE.userdocs_prefix + full_model_name(x) + '>`'
    #~ return ':ref:`' + x.verbose_name + ' <' + settings.SITE.userdocs_prefix \
        #~ + full_model_name(x.model) + '.' + x.name + '>`'
        
def actor_name(a): return settings.SITE.userdocs_prefix + str(a).lower()
def model_name(m): return settings.SITE.userdocs_prefix + full_model_name(m).lower()

def actor_ref(rpt,text=None):
    if text is None:
        text = force_unicode(rpt.label or rpt.title or str(rpt))
    return ':ref:`%s <%s>`' % (text,actor_name(rpt))

def model_ref(m,text=None):
    if text is None:
        text = force_unicode(m._meta.verbose_name)
    return ':ref:`%s <%s>`' % (text,model_name(m))

def rptlist(l):
    return ', '.join([actor_ref(a) for a in l])
    #~ return ', '.join([
        #~ ":ref:`%s (%s) <%s>`" % (str(rpt),force_unicode(rpt.label),actor_ref(rpt)) 
        #~ for rpt in l])

def fields_table(fields):
    headers = ["name","type"]
    #~ formatters = [
      #~ lambda f: f.name,
      #~ lambda f: f.__class__.__name__,
    #~ ]
    headers.append("verbose name")
    headers.append("help text")
    def fieldtype(f):
        if isinstance(f,models.ForeignKey):
            #~ return f.__class__.__name__ + " to " + refto(f.rel.to)
            return f.__class__.__name__ + " to " + model_ref(f.rel.to)
        return f.__class__.__name__
        
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
      
def get_model_description(self):
    """
    `self` is the actor
    """
    body = "\n\n"
    help_text = getattr(self,'help_text',None)
    if help_text:
        body += unindent(force_unicode(help_text).strip()) + "\n\n"

    body += fields_table(self._meta.fields)
    
    return body
    
from lino.core import actions    
    
IGNORED_ACTIONS = (actions.GridEdit,actions.SubmitDetail,
    actions.InsertRow,actions.SubmitInsert)
      
def actions_overview_ul(action_list):
    items = []
    for ba in action_list:
        desc = "[%s]" % unicode(ba.action.label)
        #~ if ba.action.action_name:
            #~ desc += " (%s)" % ba.action.action_name
        if ba.action.help_text:
            desc += " -- " + unicode(ba.action.help_text)
        items.append(desc)
    return rstgen.ul(items)
    
def actors_overview_ul(model_reports):
    items = []
    for tb in model_reports:
        desc = actor_ref(tb)
        #~ label = unicode(tb.title or tb.label)
        desc += " (%s)" % str(tb)
        if tb.help_text:
            desc += " -- " + unicode(tb.help_text)
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
            cls = settings.SITE.modules.resolve(self.content[0])
            if not isinstance(cls,type):
                raise Exception("%s is not an actor." % self.content[0])
                
            if issubclass(cls,models.Model):
                model = cls
                #~ if full_model_name(cls) == 'cal.Event':
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
                #~ s += rstgen.header(3,_('%s (%s)') % (title,full_model_name(cls)))
                s += rstgen.header(3,title)
                
                if len(self.content) > 1:
                    s += '\n'.join(self.content[1:])
                    s += '\n\n'
                    
                s += rstgen.header(4,_("Fields of %s") % cls._meta.verbose_name)
                s += '\n'
                s += fields_table(cls._meta.fields)
                
                action_list = cls._lino_default_table.get_actions()
                action_list = [ba for ba in action_list if ba.action.sort_index <= 30]
                action_list = [ba for ba in action_list if isinstance(ba.action,IGNORED_ACTIONS)]
                if action_list:
                    s += '\n'
                    s += rstgen.header(4,_("Actions on a %s") % cls._meta.verbose_name)
                    s += actions_overview_ul(action_list)
                    
                model_reports = [r for r in dbtables.master_reports if r.model is cls]
                model_reports += [r for r in dbtables.slave_reports if r.model is cls]
                
                s += '\n'
                s += rstgen.header(4,_("Tables based on %s") % cls._meta.verbose_name_plural)
                
                #~ for tb in model_reports:
                    #~ s += '\n\n.. _'+ actor_name(tb) + ':\n\n'
                    #~ label = unicode(tb.title or tb.label)
                    #~ s += rstgen.header(5,label)
                    #~ s += "%s : %s\n" % (unicode(_('Internal name')),tb)
                    #~ if tb.help_text:
                        #~ s += '\n'
                        #~ s += unicode(tb.help_text)
                    #~ s += '\n'
                    
                s += actors_overview_ul(model_reports)
                    
                slave_tables = getattr(cls,'_lino_slaves',{}).values()
                if slave_tables:
                    #~ for tb in slave_tables:
                        #~ s += '\n.. _'+ settings.SITE.userdocs_prefix + str(tb) + ':\n'
                    s += '\n'
                    s += rstgen.header(4,_("Slave tables of %s") % cls._meta.verbose_name)
                    s += actors_overview_ul(slave_tables)
                    
                
                #~ if model_reports:
                    #~ s += '\nMaster tables: %s\n' % rptlist(model_reports)
                #~ if slave_tables:
                    #~ s += '\nSlave tables: %s\n' % rptlist(slave_tables)
    
                return s
                
            if issubclass(cls,actors.Actor):
              
                #~ if issubclass(cls,dbtables.Table):
                    #~ if cls.model is not None:
                        #~ if cls.model.get_default_table() is cls:
                            #~ self.add_model_index_entry(cls.model)
                            #~ name = settings.SITE.userdocs_prefix + full_model_name(cls.model)
                            #~ s += '\n\n.. _'+ name + ':\n\n'
                        
              
                title = force_unicode(cls.label or cls.title)
                indextext = _('%s (table in module %s)') % (title,cls.app_label)
                name = actor_name(cls)
                self.index_entries.append(('single', indextext, name, ''))
                #~ self.add_ref_target(name,name)
                
                s = ''
                s += '\n\n.. _'+ name + ':\n\n'
                s += rstgen.header(3,title)
                
                if len(self.content) > 1:
                    s += '\n'.join(self.content[1:])
                    s += '\n\n'
                
                s += '\n\n'
                s += get_actor_description(cls)
                s += '\n\n'
                return s
            raise Exception("Cannot handle actor %r." % cls)
            
    def unused_add_ref_target(self, fullname,localname):
        #~ fullname = settings.SITE.userdocs_prefix  + str(cls)
        #~ modname = self.options.get(
            #~ 'module', self.env.temp_data.get('py:module'))
        #~ fullname = (modname and modname + '.' or '') + name_cls[0]
        # note target
        
        if fullname not in self.state.document.ids:
            #~ signode['names'].append(fullname)
            #~ signode['ids'].append(fullname)
            #~ signode['first'] = (not self.names)
            #~ self.state.document.note_explicit_target(signode)
            objects = self.env.domaindata['py']['objects']
            if fullname in objects:
                self.state_machine.reporter.warning(
                    'duplicate object description of %s, ' % fullname +
                    'other instance in ' +
                    self.env.doc2path(objects[fullname][0]) +
                    ', use :noindex: for one of them',
                    line=self.lineno)
            objects[fullname] = (self.env.docname, localname)

        
    def unused_add_model_index_entry(self,model):
        title = force_unicode(model._meta.verbose_name)
        indextext = _('%s (model in module `%s`)') % (title,model._meta.app_label)
        name = model_name(model)
        labelid = fully_normalize_name(name)
        #~ name = name.lower()
        #~ labelid = name.replace('.','-')
        self.index_entries.append(('single', indextext, name, ''))
        #~ self.add_ref_target(name,'model')
        
        env = self.env
        labels = env.domaindata['std']['labels'] 
        # a dict mapping labelname -> docname, labelid, sectionname
        labels[name] = (self.env.docname,labelid,title)
        
        env.domaindata['std']['anonlabels'][name] = (self.env.docname,labelid)
        
        #~ print '20130408 %s --> %s' % (name,  title)
        
    
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
        
        x = settings.SITE.modules.resolve(target)
        if x is None:
            raise Exception("Could not resolve name %r" % target)
        if issubclass(x,models.Model):
            text = utils.unescape(unicode(x._meta.verbose_name))
            target = model_name(x)
        elif issubclass(x,actors.Actor):
            text = utils.unescape(unicode(x.title or x.label))
            target = actor_name(x)
            
        else:
            raise Exception("Don't know how to handle %r" % x)
        
        if not has_explicit_title:
            title = text
            
        #~ refnode['reftype'] = 'ref'
        
        return title, target


def setup(app):
    
    app.add_directive('actor', ActorDirective)
    app.add_directive('actors_overview', ActorsOverviewDirective)
    app.add_role('ddref', ddrefRole(warn_dangling=True))
