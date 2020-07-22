# -*- coding: UTF-8 -*-
# Copyright 2013-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""
A Sphinx extension used to write multilingual user documentation
for a Lino application.

.. rst:directive:: lino2rst

  Execute Python code and process the output as reStructuredText
  source code.  This is like :rst:dir:`py2rst` but with the following
  names defined:

  :settings: The Django settings module which is active while building
             the docs.

  :dd: The :mod:`lino.api.dd` module.

  :rt: The :mod:`lino.api.rt` module.

  Plus the app_label of each installed plugin.


.. rst:directive:: fields_list

   Render a bullet list of the fields in a given model.  The first
   word of the content is the model. If there are any other words,
   then these are field names.  If no field names are specified, all
   fields of the model are included.

.. rst:role:: menupath

   Render the given menu command specifier as a `menuselection` role.

.. rst:directive:: actor

Usage::

  .. actor:: app_name[.ActorName][.data_element_name]

    Optional introduction text.

Insert the full description of the specified data dictionary item.  If
the name contains no ".", then it is the name of a Plugin.  If the
name contains one ".", then it is the name of an Actor or a Model.  If
the name contains two ".", then it is the name of a data element of
that Actor or Model (data elements can be fields or actions)

.. rst:role:: ddref

(Deprecated) Insert a reference to the named data dictionary item.
The visible text will be automatically in the right language in
multilingual userdocs.
"""

from __future__ import unicode_literals, print_function
from builtins import str

from .base import menuselection_text

from docutils.parsers.rst import Directive
# from sphinx.util.compat import Directive


from sphinx.roles import XRefRole, menusel_role
from sphinx.util import ws_re
from sphinx import addnodes

from docutils import nodes, utils
from docutils.nodes import fully_normalize_name

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils import translation
from django.utils.encoding import force_text

from lino.api import dd, rt

from lino.core import actors
from lino.core import actions
from lino.core import choicelists
from lino.core import kernel
from rstgen.utils import unindent
import rstgen
from lino.core.utils import full_model_name
from lino.ad import Plugin
from lino.utils.diag import analyzer
from lino.core.actors import resolve_action
from lino.modlib.users.choicelists import UserTypes

from atelier.sphinxconf.insert_input import Py2rstDirective


def actor_name(a):
    return fully_normalize_name(settings.SITE.userdocs_prefix + str(a))


def model_name(m):
    return settings.SITE.userdocs_prefix + full_model_name(m).lower()


def app_name(a):
    assert a.__name__.endswith('.models')
    parts = a.__name__.split('.')
    return settings.SITE.userdocs_prefix + parts[-2]


def actor_ref(rpt, text=None):
    if text is None:
        text = force_text(rpt.label or rpt.title or str(rpt))
    return ':ddref:`%s <%s>`' % (text, rpt)


def model_ref(m, text=None):
    if text is None:
        text = force_text(m._meta.verbose_name)
    return ':ref:`%s <%s>`' % (text, model_name(m))


def rptlist(l):
    return ', '.join([actor_ref(a) for a in l])


def typeref(cls):
    text = cls.__name__
    target = cls.__module__ + '.' + cls.__name__
    return ":class:`%s <%s>`" % (text, target)


def old_fieldtype(f):
    if isinstance(f, models.ForeignKey):
        #~ return f.__class__.__name__ + " to " + refto(f.rel.model)
        return f.__class__.__name__ + " to " + model_ref(f.remote_field.model)
    return f.__class__.__name__


def fieldtype(f):
    s = typeref(f.__class__)
    if isinstance(f, models.ForeignKey):
        s = _("%(classref)s to %(model)s") % dict(
            classref=s, model=model_ref(f.remote_field.model))
        #~ print(20130908, s)
    if isinstance(f, choicelists.ChoiceListField):
        s = _("%(classref)s to %(model)s") % dict(
            classref=s, model=actor_ref(f.choicelist))
    return s


def fields_ul(fields):
    helpless = []

    def field2li(fld):
        s = "**%s**" % str(f.verbose_name).strip()
        s += " (``%s``, %s)" % (f.name, fieldtype(f))
        if f.help_text:
            s += " -- " + str(f.help_text)
            return s
        helpless.append(s)
        return None

    items = []
    for f in fields:
        if not hasattr(f, '_lino_babel_field'):
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
    headers = ["name", "type"]
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
            #~ cells.append(force_text(_(f.verbose_name)))
        #~ cells.append(f.help_text)
        return cells
    rows = [rowfmt(f) for f in fields if not hasattr(f, '_lino_babel_field')]
    return rstgen.table(headers, rows)


def get_actor_description(self):
    """
    `self` is the actor
    """
    body = "\n\n"
    if self.help_text:
        body += unindent(force_text(self.help_text).strip()) + "\n\n"

    #~ ll = self.get_handle().list_layout
    #~ if ll is not None:
        #~ body += fields_table([ e.field for e in ll.main.columns] )

    #~ model_reports = [r for r in kernel.master_tables if r.model is self.model]
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
        #~ body += unindent(force_text(help_text).strip()) + "\n\n"
#~
    #~ body += fields_table(self._meta.fields)
    #~
    #~ return body


IGNORED_ACTIONS = (actions.ShowTable, actions.SubmitDetail,
                   actions.ShowDetail,
                   actions.DeleteSelected,
                   actions.ShowInsert, actions.SubmitInsert)

def menuselection(mi):
    return ":menuselection:`%s`" % menuselection_text(mi)


def actions_ul(action_list):
    items = []
    for ba in action_list:
        label = ba.action.label
        desc = "**%s** (" % str(label).strip()
        if ba.action.action_name:
            desc += "``%s``" % ba.action.action_name

        desc += ", %s)" % typeref(ba.action.__class__)
        if ba.action.help_text:
            desc += " -- " + str(ba.action.help_text)
        items.append(desc)
    return rstgen.ul(items)

# from lino.core.menus import find_menu_item


def actors_overview_ul(model_reports):
    user_type = UserTypes.get_by_value('900')
    # deprecated
    items = []
    for tb in model_reports:
        desc = actor_ref(tb)
        #~ label = str(tb.title or tb.label)
        #~ desc += " (%s)" % str(tb)
        desc += " (%s)" % typeref(tb)
        # mi = find_menu_item(tb.default_action)
        mi = user_type.find_menu_item(tb.default_action)
        if mi is not None:
            desc += _(" (Menu %s)") % menuselection(mi)
            #~ print(unicode(mi.label).strip())
        if tb.help_text:
            desc += " -- " + str(tb.help_text).strip()

        items.append(desc)
    return rstgen.ul(items)


def resolve_name(name):
    l = name.split('.')
    if len(l) == 1:
        return 1, settings.SITE.plugins.get(name)
        # return 1, dd.resolve_app(name)
    if len(l) == 3:
        model = settings.SITE.models.resolve(l[0] + '.' + l[1])
        if model is None:
            raise Warning("Unkown name %s" % name)
        return 3, model.get_data_elem(l[2])
    return len(l), settings.SITE.models.resolve(name)


def form_lines():
    yield '<script >'


class ddrefRole(XRefRole):

    nodeclass = addnodes.pending_xref
    innernodeclass = nodes.emphasis

    def __call__(self, typ, rawtext, text, lineno, inliner,
                 options={}, content=[]):

        typ = 'std:ref'
        self._reporter = inliner.document.reporter
        self._lineno = lineno
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

        target = ws_re.sub(' ', target)  # replace newlines or tabs by spaces
        # ~ target = ' '.join(target.split()) # replace newlines or tabs by spaces

        level, x = resolve_name(target)
        if x is None:
            msg = "Could not resolve name %r" % target
            return [self._reporter.warning(msg, line=self._lineno), target]
            # raise Exception(msg)
        # lng = env.temp_data.get('language', env.config.language)
        lng = CurrentLanguage.get_current_value(env)
        with translation.override(lng):
            if isinstance(x, models.Field):
                text = utils.unescape(str(x.verbose_name))
                target = model_name(x.model) + '.' + x.name
                # print(target)
            elif isinstance(x, Plugin):
                text = utils.unescape(str(x.verbose_name))
                target = settings.SITE.userdocs_prefix + target

            elif isinstance(x, type) and issubclass(x, models.Model):
                text = utils.unescape(str(x._meta.verbose_name))
                target = model_name(x)
            elif isinstance(x, type) and issubclass(x, actors.Actor):
                text = utils.unescape(str(x.title or x.label))
                target = actor_name(x)
            elif isinstance(x, actions.Action):
                text = utils.unescape(str(x.label))
                target = actor_name(x)
            else:
                raise Exception("Don't know how to handle %r" % x)

        if not has_explicit_title:
            # avoid replacing title by the heading text
            refnode['refexplicit'] = True
            title = text

        refnode['refwarn'] = False  # never warn

        #~ refnode['reftype'] = 'ref'

        #~ title = "[%s]" % title
        #~ if target == 'welfare.reception.waitingvisitors':
        #~ print("20130907 ddref to %s : title=%r" % (target,title))

        return title, target


class TempDataDirective(Directive):
    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {}
    temp_data_key = None

    @classmethod
    def get_default_value(self, env):
        return None

    @classmethod
    def get_current_value(cls, env):
        return env.temp_data.get(
            cls.temp_data_key,
            cls.get_default_value(env))

    def run(self):
        env = self.state.document.settings.env
        v = self.arguments[0].strip()
        if v == 'None':
            del env.temp_data[self.temp_data_key]
        else:
            env.temp_data[self.temp_data_key] = v
        return []


class CurrentLanguage(TempDataDirective):
    """Tell Sphinx to switch to the specified language until the end of
    this document.

    """
    temp_data_key = 'language'

    @classmethod
    def get_default_value(cls, env):
        return env.config.language


class CurrentProject(TempDataDirective):
    """Tell Sphinx to switch to the specified project until the end of
    this document.

    """
    temp_data_key = 'lino_project'


class Lino2rstDirective(Py2rstDirective):
    """Defines the :rst:dir:`lino2rst` directive."""

    def get_context(self):
        from django.conf import settings
        context = super(Lino2rstDirective, self).get_context()
        context.update(settings=settings)
        context.update(settings.SITE.models)
        context.update(dd=dd)
        context.update(rt=rt)
        return context

    def output_from_exec(self, code):
        from django.utils import translation
        with translation.override(self.language):
            return super(Lino2rstDirective, self).output_from_exec(code)


class ActorsOverviewDirective(Lino2rstDirective):

    def get_rst(self):
        user_type = UserTypes.get_by_value('900')
        with translation.override(self.language):
            #~ set_language(lng)
            actor_names = ' '.join(self.content).split()
            items = []
            for an in actor_names:
                cls = settings.SITE.models.resolve(an)
                if not isinstance(cls, type):
                    raise Exception("%s is not an actor." % self.content[0])
                desc = "**{0}** (:class:`{1} <{2}>`)".format(
                    force_text(cls.label),
                    cls.__name__,
                    cls.__module__ + '.' + cls.__name__
                )
                mi = user_type.find_menu_item(cls.default_action)
                if mi is not None:
                    desc += _(" (Menu %s)") % menuselection(mi)
                    #~ print(str(mi.label).strip())
                if cls.help_text:
                    desc += "  : " + force_text(cls.help_text).strip()

                # items.append("%s : %s" % (actor_ref(cls), cls.help_text or ''))
                items.append(desc)
            return rstgen.ul(items)


class ShowFieldsDirective(Lino2rstDirective):

    def get_rst(self):
        with translation.override(self.language):
            names = ' '.join(self.content).split()
            if len(names) > 1:
                field_names = ' '.join(names[1:])
            else:
                field_names = None
            return analyzer.show_fields(
                names[0], field_names=field_names)


class FormDirective(Lino2rstDirective):

    def get_rst(self):
        level, cls = resolve_name(self.content[0])
        s = ''
        with translation.override(self.language):
            s = '\n'.join(list(form_lines()))
        return s


class ActorDirective(Lino2rstDirective):
    #~ has_content = False
    titles_allowed = True
    #~ debug = True

    def get_rst(self):
        #~ from actordoc import get_actor_description
        #~ from django.conf import settings
        #~ from djangosite.dbutils import set_language
        with translation.override(self.language):
            level, cls = resolve_name(self.content[0])
            if isinstance(cls, models.Field):
                fld = cls
                s = ''
                name = str(fld.model) + '.' + fld.name
                title = force_text(fld.verbose_name).strip()

                s += "\n.. index::\n   single: "
                s += str(_('%(field)s (field in %(model)s)') % dict(
                    field=title, model=model_ref(fld.model)))
                s += '\n\n'
                s += rstgen.header(level, _("%s (field)") % title)
                if len(self.content) > 1:
                    s += '\n'.join(self.content[1:])
                    s += '\n\n'
                return s

            if isinstance(cls, Plugin):
                s = ''
                title = str(cls.verbose_name)
                s += "\n.. index::\n   single: "
                s += str(_('%s (app)') % title)
                s += '\n\n.. _' + name + ':\n'
                s += '\n'
                s += rstgen.header(level, _("%s (app)") % title)
                return s

            if not isinstance(cls, type):
                raise Exception("%s is not an actor." % self.content[0])

            if issubclass(cls, models.Model):
                model = cls

                s = ''
                name = model_name(model).lower()
                title = force_text(model._meta.verbose_name)
                s += "\n.. index::\n   single: "
                s += str(_('%(model)s (model in %(app)s)') % dict(
                    model=title, app=model._meta.app_label))

                s += '\n\n'

                s += '\n\n.. _' + name + ':\n'

                s += '\n'
                s += rstgen.header(level, _("%s (model)") % title)

                s += '\n'
                s += '\n:Internal name: ``%s``\n' % full_model_name(cls)
                s += '\n:Implemented by: %s\n' % typeref(cls)
                s += '\n'

                if len(self.content) > 1:
                    s += '\n'.join(self.content[1:])
                    s += '\n\n'

                model_reports = [
                    r for r in kernel.master_tables if r.model is cls]
                model_reports += [r for r in kernel.slave_tables
                                  if r.model is cls]
                s += rstgen.boldheader(_("Views on %s") %
                                       cls._meta.verbose_name)
                s += actors_overview_ul(model_reports)

                s += rstgen.boldheader(_("Fields in %s") %
                                       cls._meta.verbose_name)
                s += fields_ul(cls._meta.fields)

                action_list = cls.get_default_table().get_actions()
                action_list = [
                    ba for ba in action_list
                    if not isinstance(ba.action, IGNORED_ACTIONS)]
                if action_list:
                    s += '\n'
                    s += rstgen.boldheader(_("Actions on %s") %
                                           cls._meta.verbose_name)
                    s += actions_ul(action_list)

                slave_tables = getattr(cls, '_lino_slaves', {}).values()
                if slave_tables:
                    s += rstgen.boldheader(_("Tables referring to %s") %
                                           cls._meta.verbose_name)
                    s += actors_overview_ul(slave_tables)

                return s

            if issubclass(cls, actors.Actor):

                title = force_text(cls.label or cls.title)
                indextext = _('%(actor)s (view in %(app)s)') % dict(
                    actor=title, app=cls.app_label)
                name = actor_name(cls)
                #~ if name == 'welfare.reception.waitingvisitors':
                    #~ self.debug = True
                #~ print(20130907, name)
                self.index_entries.append(('single', indextext, name, ''))
                #~ self.add_ref_target(name,name)

                s = ''
                s += '\n\n.. _%s:\n\n' % name
                s += rstgen.header(level, _("%s (view)") % title)
                s += '\n:Internal name: ``%s`` (%s)\n' % (cls, typeref(cls))

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
        content = super(ActorDirective, self).run()
        indexnode = addnodes.index(entries=self.index_entries)
        return [indexnode] + content


def menupath_role(typ, rawtext, text, *args, **kwargs):
    a = resolve_action(text)
    user_type = UserTypes.get_by_value('900')
    mi = user_type.find_menu_item(a)
    if mi is None:
        raise Exception("Unknown menu descriptor %s" % text)
    text = menuselection_text(mi)
    rawtext = menuselection(mi)
    return menusel_role('menuselection', rawtext, text, *args, **kwargs)


def setup(app):

    app.add_directive('form', FormDirective)
    app.add_directive('actor', ActorDirective)
    app.add_directive('actors_overview', ActorsOverviewDirective)
    app.add_directive('fields_list', ShowFieldsDirective)
    app.add_role('ddref', ddrefRole())
    app.add_role('menupath', menupath_role)
    app.add_directive('currentlanguage', CurrentLanguage)
    app.add_directive('currentproject', CurrentProject)
    app.add_directive('django2rst', Lino2rstDirective)  # backward compat
    app.add_directive('lino2rst', Lino2rstDirective)
