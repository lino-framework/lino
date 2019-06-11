# -*- coding: utf-8 -*-
# Copyright 2012-2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
"""Some diagnostic utilities."""

from __future__ import unicode_literals
from builtins import str
from builtins import object
import six

# from textwrap import fill
from atelier import rstgen
from atelier.utils import unindent

from django.conf import settings
from django.utils.encoding import force_text

from lino.core.layouts import BaseLayout
from lino.core.elems import Container, Wrapper, FieldElement
from lino.modlib.users.choicelists import UserTypes
from lino.core import actors
from lino.core import actions
from lino.core.utils import get_models, sorted_models_list
from lino.core.utils import full_model_name as fmn
from lino.api import dd


class Analyzer(object):
    "The class of the :data:`lino.utils.diag.analyzer` object."
    def __init__(self):
        self._initialized = False

    def analyze(self):
        if self._initialized:
            return
        self._initialized = True
        window_actions = dict()
        self.custom_actions = []
        for a in actors.actors_list:
            if a.abstract:
                continue
            for ba in a.get_actions():
                if ba.action.is_window_action():
                    wl = ba.get_window_layout() or ba.action.params_layout
                    if wl is not None:
                        if isinstance(wl, six.string_types):
                            raise Exception("20150323 : {0}".format(ba))
                            # Was used to find Exception: 20150323 :
                            # <BoundAction(checkdata.Checkers,
                            # <ShowDetail detail (u'Detail')>)>

                        if wl not in window_actions:
                            # lh = wl.get_layout_handle(ui)
                            # for e in lh.main.walk():
                            #     e.loosen_requirements(a)
                            window_actions[wl] = ba
                else:  # if ba.action.custom_handler:
                    self.custom_actions.append(ba)
        l = list(window_actions.values())

        def f(a):
            return str(a.full_name())
        self.window_actions = list(sorted(l, key=f))
        self.custom_actions = list(sorted(self.custom_actions, key=f))
    
    def show_window_fields(self):
        self.analyze()
        items = []
        for ba in analyzer.window_actions:
            items.append(
                "{0} : {1}".format(
                    ba.full_name(), layout_fields(ba)))

        return rstgen.ul(items)

    def show_window_permissions(self):
        self.analyze()
        items = []
        for ba in analyzer.window_actions:
            items.append(
                "{0} : visible for {1}".format(
                    ba.full_name(), visible_for(ba)))

        return rstgen.ul(items)
    
    def show_memo_commands(self, doctestfmt=False):
        rst = ""
        mp = settings.SITE.kernel.memo_parser
        items = []
        for cmd, func in sorted(mp.commands.items()):
            doc = unindent(func.__doc__ or '')
            if doc:
                # doc = doc.splitlines()[0]
                items.append(
                    "[{0} ...] : {1}".format(cmd, doc))
            
        # rst += "\n**Commands**"
        # rst += rstgen.boldheader("Commands")
        rst += rstgen.ul(items)

        if False:
            items = []
            for model, func in sorted(mp.renderers.items()):
                doc = unindent(func.__doc__ or '')
                if doc:
                    items.append(
                        "[{0} ...] : {1}".format(model, doc))
            if len(items):
                rst += "\n**Renderers**"
                rst += rstgen.ul(items)
        

        return rst
    
    def show_dialog_actions(self, doctestfmt=False):
        self.analyze()
        items = []
        for ba in analyzer.custom_actions + analyzer.window_actions:
            if ba.action.parameters:
                items.append(
                    "{0} : {1}".format(
                        ba.full_name(),
                        py2rst(ba.action, doctestfmt)))

        print(rstgen.ul(items))
    
    def show_action_permissions(self, *classes):
        self.analyze()
        items = []
        for ba in analyzer.custom_actions + analyzer.window_actions:
            if isinstance(ba.action, classes):
                items.append(
                    "{0} : visible for {1}".format(
                        ba.full_name(), visible_for(ba)))

        return rstgen.ul(items)
    
    def show_database_structure(self):
        """Show a bullet list of all models and their fields."""
        self.analyze()
        items = []
        for model in get_models():
            names = []
            # for f, m in model._meta.get_fields_with_model():
            for f in model._meta.concrete_fields:
                names.append(f.name)
            items.append(
                "{0} : {1}".format(fmn(model), ', '.join(names)))

        items = sorted(items)
        return rstgen.ul(items)

    def show_fields(self, model, field_names=None, languages=None):
        model = dd.resolve_model(model)
        if field_names is not None:
            field_names = dd.fields_list(model, field_names)
        items = []
        for f in model._meta.fields:
            if field_names is None or f.name in field_names:
                name = f.name
                ref = model.__module__ + '.' + model.__name__ + '.' + name
                verbose_name = force_text(f.verbose_name).strip()
                help_text = force_text(f.help_text).replace('\n', ' ')
                txt = "**{verbose_name}** (:attr:`{name} <{ref}>`) : " \
                      "{help_text}".format(**locals())
                items.append(txt)
        return rstgen.ul(items)

    def show_db_overview(self):
        """Return a reStructredText-formatted "database overview" report.
        Used by test cases in tested documents.

        """

        models_list = sorted_models_list()
        apps = [p.app_label for p in settings.SITE.installed_plugins]
        s = "%d apps: %s." % (len(apps), ", ".join(apps))
        s += "\n%d models:\n" % len(models_list)
        i = 0
        headers = [
            #~ "No.",
            "Name",
            "Default table",
            #~ "M",
            "#fields",
            "#rows",
            #~ ,"first","last"
        ]
        rows = []
        for model in models_list:
            if True:  # model._meta.managed:
                i += 1
                cells = []
                #~ cells.append(str(i))
                cells.append(fmn(model))
                cells.append(model.get_default_table())
                #~ cells.append(str(model))
                #~ if model._meta.managed:
                #~ cells.append('X')
                #~ else:
                #~ cells.append('')
                cells.append(str(len(model._meta.concrete_fields)))
                qs = model.objects.all()
                n = qs.count()
                cells.append(str(n))
                #~ if n:
                #~ cells.append(obj2str(qs[0]))
                #~ cells.append(obj2str(qs[n-1]))
                #~ else:
                #~ cells.append('')
                #~ cells.append('')

                rows.append(cells)
        s += rstgen.table(headers, rows)
        return s

    def show_foreign_keys(self):
        """Return a list that shows how database objects are being referred to
        by some other database object. This information is important
        (1) before deleting objects and (2) when merging them.

        For every model we see a list of "delete handlers" and a list
        of fields from other models that point to this model using
        that delete handler.

        Delete handlers are:

        - PROTECT : refuse to delete when other objects refer to this object
        - CASCADE : delete objects refering to this object
        - set_on_delete : make other objects point to something else (or set
          their pointer to None)

        """
        self.analyze()
        tdp = dict()  # target model -> delete handler -> pointer list
        for target in get_models():
            dp = tdp.setdefault(target, dict())
            for m, fk in target._lino_ddh.fklist:
                k = fk.remote_field.on_delete
                p = dp.setdefault(k, [])
                p.append((m, fk))

        def fk2str(mfk):
            return "{0}.{1}".format(fmn(mfk[0]), mfk[1].name)

        items1 = []
        for target, dp in list(tdp.items()):
            items2 = []
            for dh, pl in list(dp.items()):
                items2.append(
                    "{0} : {1}".format(
                        dh.__name__, ', '.join([fk2str(mfk) for mfk in pl])))
            if len(items2):
                items2 = sorted(items2)
                items1.append("{0} :\n{1}".format(
                    fmn(target), rstgen.ul(items2)))
    
        items1 = sorted(items1)
        return rstgen.ul(items1)

    def show_complexity_factors(self):
        self.analyze()
        items = []
        items.append("{0} plugins".format(len(dd.plugins)))
        items.append("{0} models".format(len(get_models())))
        items.append("{0} user roles".format(
            len(settings.SITE.user_roles)))
        items.append("{0} user types".format(len(UserTypes.objects())))
        items.append("{0} views".format(len(
            [a for a in actors.actors_list if not a.abstract])))
        dialog_actions = [ba for ba in analyzer.custom_actions +
                          analyzer.window_actions if
                          ba.action.parameters]
        items.append("{0} dialog actions".format(len(dialog_actions)))
        return rstgen.ul(items)
        
    
def visible_for(ba):
    """Shows a list of user profiles for which this action is visible."""
    if ba is None:
        return "N/A"
    if isinstance(ba, type)  and issubclass(ba, actors.Actor):
        ba = ba.default_action
    visible = []
    hidden = []
    for p in UserTypes.objects():
        name = p.name or p.value
        if ba.get_view_permission(p):
            visible.append(name)
        else:
            hidden.append(name)
    if len(hidden) == 0:
        return "all"
    if len(visible) == 0:
        return "nobody"
    # if len(hidden) < len(visible):
    # if len(hidden) <= 3:
    #     return "all except %s" % ', '.join(hidden)
    return ' '.join(visible)


def layout_fields(ba):
    wl = ba.get_window_layout() or ba.action.params_layout
    if wl is None:
        return ''
    lh = wl.get_layout_handle(settings.SITE.kernel.default_ui)
    elems = [str(f.name) for f in lh._store_fields]
    return ', '.join(elems)
    # return fill(' '.join(elems), 50)


def py2rst(self, doctestfmt=False):
    """Render any Python object as reStructuredText.

    Where "any" currently means a layout or a layout element.
    :class:`lino.core.layouts.BaseLayout`
    :mod:`lino.modlib.extjs.elems`

    If the optional argument `doctestfmt` is specified as `True`, then
    output contains less blank lines which might be invalid
    reStructuredText but is more doctest-friendly.

    """
    if isinstance(self, actions.Action):
        s = str(self)
        if self.params_layout:
            lh = self.params_layout.get_layout_handle(
                settings.SITE.kernel.default_ui)
            s += '\n'
            s += py2rst(lh.main, doctestfmt)
        return s

    if isinstance(self, BaseLayout):
        lh = self.get_layout_handle(settings.SITE.kernel.default_ui)
        return py2rst(lh.main, doctestfmt)
        
    if isinstance(self, Wrapper):
        self = self.wrapped

    if isinstance(self, FieldElement):
        s = "**%s** (%s)" % (str(self.field.verbose_name), self.field.name)
    elif self.get_label() is None:
        s = "(%s)" % self.name
    else:
        s = "**%s** (%s)" % (str(self.get_label()), self.name)
    if visible_for(self) != visible_for(self.parent):
        s += " [visible for %s]" % visible_for(self)
    if isinstance(self, Container):
        use_ul = False
        for e in self.elements:
            if isinstance(e, Container):
                use_ul = True
        children = [py2rst(e, doctestfmt) for e in self.elements]
        if len(children):
            if use_ul:
                s += ':\n'
                if not doctestfmt:
                    s += '\n'
                s += rstgen.ul(children)
            else:
                s += ": " + ', '.join(children)
                
    return s


analyzer = Analyzer()
"""This is a docstring
"""


