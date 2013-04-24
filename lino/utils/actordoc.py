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

from sphinx.ext.autodoc import ModuleLevelDocumenter
from sphinx.util.docstrings import prepare_docstring
from sphinx.util import force_decode


from sphinx.roles import XRefRole
#~ from sphinx.config import Config
#~ from sphinx.errors import SphinxError, SphinxWarning, ExtensionError, \
     #~ VersionRequirementError
from sphinx.domains import ObjType
#~ from sphinx.domains.std import GenericObject, Target, StandardDomain
from sphinx.domains.std import StandardDomain
from sphinx.domains.python import PyModulelevel
from sphinx import addnodes


from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_unicode



from lino.core import actors
from lino.core import choicelists
from lino.core import dbtables
from atelier.utils import unindent
from atelier import rstgen
from djangosite.dbutils import full_model_name
from djangosite.dbutils import set_language

from atelier.sphinxconf import Django2rstDirective


import lino.ui.urls # hack: trigger ui instantiation


def refto(x):
    if x is None: 
        return '`None`'
    if issubclass(x,models.Model):
        #~ return ':ref:`' + x.__name__ + ' <' + full_model_name(x) + '>`'
        return ':ref:`' + force_unicode(x._meta.verbose_name) + ' <' \
            + settings.SITE.userdocs_prefix + full_model_name(x) + '>`'
    #~ if isinstance(x,Field):
    return ':ref:`' + x.verbose_name + ' <' + settings.SITE.userdocs_prefix \
        + full_model_name(x.model) + '.' + x.name + '>`'
        
def actor_ref(rpt):
    label = force_unicode(rpt.label or rpt.title or str(rpt))
    target = settings.SITE.userdocs_prefix + str(rpt)
    #~ return label
    return ':ref:`%s <%s>`' % (label,target)

def model_ref(m):
    label = force_unicode(m._meta.verbose_name)
    #~ target = settings.SITE.userdocs_prefix + full_model_name(m)
    target = settings.SITE.userdocs_prefix + str(m._lino_default_table)
    #~ return label
    return ':ref:`%s <%s>`' % (label,target)

def rptlist(l):
    return ', '.join([actor_ref(a) for a in l])
    #~ return ', '.join([
        #~ ":ref:`%s (%s) <%s>`" % (str(rpt),force_unicode(rpt.label),actor_ref(rpt)) 
        #~ for rpt in l])




def get_actor_description(self):
    """
    `self` is the actor
    """
    body = "\n\n"
    if self.help_text:
        body += unindent(force_unicode(self.help_text).strip()) + "\n\n"

    ll = self.get_handle().list_layout
    if ll is not None:
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
        #~ rows = [ rowfmt(f) for f in self.model._meta.fields if not hasattr(f,'_lino_babel_field')]
        rows = [ rowfmt(e.field) for e in ll.main.columns 
            if not hasattr(e.field,'_lino_babel_field')]
        body += rstgen.table(headers,rows)
    
    #~ model_reports = [r for r in dbtables.master_reports if r.model is self.model]
    #~ if model_reports:
        #~ body += '\n\nMaster tables: %s\n\n' % rptlist(model_reports)
    #~ if getattr(model,'_lino_slaves',None):
        #~ body += '\n\nSlave tables: %s\n\n' % rptlist(model._lino_slaves.values())
    
    return body
      

if False:
  
    class ActorDocumenter(ModuleLevelDocumenter):
        objtype = 'actor'
        directivetype = 'table'
        titles_allowed = True
        
        #~ @classmethod
        #~ def can_document_member(cls, member, membername, isattr, parent):
            #~ return isinstance(member, type) and issubclass(member,actors.Actor)
            
            
        def parse_name(self):
            """Determine what module to import and what attribute to document.

            Returns True and sets *self.modname*, *self.objpath*, *self.fullname*,
            *self.args* and *self.retann* if parsing and resolving was successful.
            """
            # first, parse the definition -- auto directives for classes and
            # functions can contain a signature which is then used instead of
            # an autogenerated one
            app_label, actor_name = self.name.split('.')
            self.modname = app_label
            self.objpath = [actor_name]
            self.args = None
            self.retann = None
            self.fullname = self.name
            
            return True
            
        
        def import_object(self):
            #~ raise Exception("20130402 %s" % self.name)
            return settings.SITE.modules.resolve(self.name)
            #~ print 20130402
            #~ return super(ActorDocumenter,self).import_object()
            
        def generate(self, *args,**kw):
            lng = self.env.config.language
            set_language(lng)
            return super(ActorDocumenter,self).generate( *args,**kw)
            

        def get_doc(self, encoding=None, ignore=1):
            cls = self.import_object()
            docstring = get_actor_description(cls)
            return [prepare_docstring(force_decode(docstring, encoding),
                                      ignore)]
            
        def add_directive_header(self, sig):
            """Add the directive header and options to the generated content."""
            #~ domain = getattr(self, 'domain', 'py')
            #~ directive = getattr(self, 'directivetype', self.objtype)
            #~ name = self.format_name()
            #~ self.add_line(u'.. %s:%s:: %s%s' % (domain, directive, name, sig),
                          #~ '<autodoc>')
            cls = self.import_object()
            title = force_unicode(cls.label or cls.title)
            L = len(title)
            self.add_line('.. _%s: ' % self.name,'<autodoc>')
            self.add_line('','<autodoc>')
            self.add_line('-'*L,'<autodoc>')
            self.add_line(title,'<autodoc>')
            self.add_line('-'*L,'<autodoc>')
            self.add_line('','<autodoc>')

    class ActorDirective(PyModulelevel):
        
        def needs_arglist(self):
            return False

        def get_index_text(self, modname, name_cls):
            #~ print 20130402, self.objtype, modname, name_cls
            return _('%s (actor in module %s)') % (name_cls[0], modname)
            #~ return PyModulelevel.get_index_text(self, modname, name_cls)
            
        #~ def add_target_and_index(self, name_cls, sig, signode):
            #~ PyModulelevel.add_target_and_index(self, name_cls, sig, signode)
            

    
    def setup(app):
        #~ app.add_object_type(directivename='table',rolename='table',indextemplate='pair: %s; table')
        app.add_autodocumenter(ActorDocumenter)
        ref_nodeclass = None
        StandardDomain.object_types['table'] = ObjType('table', 'table')
        # create a subclass of GenericObject as the new directive
        #~ new_directive = type(directivename, (GenericObject, object),
                             #~ {'indextemplate': indextemplate,
                              #~ 'parse_node': staticmethod(parse_node),
                              #~ 'doc_field_types': doc_field_types})
        StandardDomain.directives['table'] = ActorDirective
        # XXX support more options?
        StandardDomain.roles['table'] = XRefRole(innernodeclass=ref_nodeclass)    


class ActorsOverviewDirective(Django2rstDirective):
    def get_rst(self):
        lng = self.state.document.settings.env.config.language
        set_language(lng)
        actor_names = ' '.join(self.content).split()
        items = []
        for an in actor_names:
            cls = settings.SITE.modules.resolve(an)
            if not isinstance(cls,type):
                raise Exception("%s is not an actor." % self.content[0])
            items.append("%s : %s" % (actor_ref(cls),cls.help_text or ''))
        return rstgen.ul(items)
    
class LinoTableDirective(Django2rstDirective):
    #~ has_content = False
    titles_allowed = True
    #~ debug = True
    def get_rst(self):
        #~ from actordoc import get_actor_description
        #~ from django.conf import settings
        #~ from djangosite.dbutils import set_language

        lng = self.state.document.settings.env.config.language
        set_language(lng)
        cls = settings.SITE.modules.resolve(self.content[0])
        if not isinstance(cls,type):
            raise Exception("%s is not an actor." % self.content[0])
        if issubclass(cls,actors.Actor):
          
            if issubclass(cls,dbtables.Table):
                if cls.model is not None:
                    if cls.model._lino_default_table is cls:
                        self.add_model_index_entry(cls.model)
                        #~ name = settings.SITE.userdocs_prefix + full_model_name(cls.model)
                        #~ s += '\n\n.. _'+ name + ':\n\n'
                    
          
            title = force_unicode(cls.label or cls.title)
            indextext = _('%s (table in module %s)') % (title,cls.app_label)
            name = settings.SITE.userdocs_prefix + str(cls)
            self.index_entries.append(('single', indextext, name, ''))
            self.add_ref_target(name)
            
            s = ''
            s += '\n\n.. _'+ settings.SITE.userdocs_prefix + str(cls) + ':\n\n'
            s += rstgen.header(3,title)
            s += '\n\n'
            s += get_actor_description(cls)
            s += '\n\n'
            return s
        raise Exception("Cannot handle actor %r." % cls)
            
    def add_ref_target(self, fullname):
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
            objects[fullname] = (self.env.docname, 'actor')

        
    def add_model_index_entry(self,model):
        title = force_unicode(model._meta.verbose_name)
        indextext = _('%s (model in module %s)') % (title,model._meta.app_label)
        name = settings.SITE.userdocs_prefix + full_model_name(model)
        name = name.lower()
        labelid = name.replace('.','-')
        self.index_entries.append(('single', indextext, name, ''))
        #~ self.add_ref_target(name)
        
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
        content = super(LinoTableDirective,self).run()
        indexnode = addnodes.index(entries=self.index_entries)
        return [indexnode] + content
        
        

def setup(app):
    
    app.add_directive('actor', LinoTableDirective)
    app.add_directive('actors_overview', ActorsOverviewDirective)
