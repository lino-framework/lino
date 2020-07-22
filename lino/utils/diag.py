# -*- coding: utf-8 -*-
# Copyright 2012-2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
"""Some diagnostic utilities."""

# from textwrap import fill
import rstgen
from rstgen.utils import unindent

from django.conf import settings
from django.db import models
from django.utils.encoding import force_text

from lino.modlib.system.choicelists import PeriodEvents
from lino.core.layouts import BaseLayout
from lino.core.layouts import ParamsLayout
from lino.core.fields import DummyField
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
                        if isinstance(wl, str):
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
        """List all window actions and the form fields they contain.
        """
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
        mp = settings.SITE.plugins.memo.parser
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
            # if ba.action.parameters and not ba.action.no_params_window:
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

    def get_complexity_factors(self, today=None):
        self.analyze()
        yield "{0} plugins".format(len(dd.plugins))
        yield "{0} models".format(len(get_models()))
        User = settings.SITE.user_model
        if today and User:
            qs = User.objects.filter(username__isnull=False)
            qs = PeriodEvents.active.add_filter(qs, today)
            yield "{0} users".format(qs.count())
        yield "{0} user roles".format(len(settings.SITE.user_roles))
        yield "{0} user types".format(len(UserTypes.objects()))
        yield "{0} views".format(len(
            [a for a in actors.actors_list if not a.abstract]))
        dialog_actions = [ba for ba in analyzer.custom_actions +
                          analyzer.window_actions
                          if ba.action.parameters and not ba.action.no_params_window]
        yield "{0} dialog actions".format(len(dialog_actions))

    def show_complexity_factors(self):
        return rstgen.ul(list(self.get_complexity_factors()))


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
    elems = [str(f.name) for f in lh._store_fields if not isinstance(f, DummyField)]
    return ', '.join(elems)
    # return fill(' '.join(elems), 50)

def elem_label(e):
    if isinstance(e, FieldElement):
        return "**%s** (%s)" % (str(e.field.verbose_name), e.field.name)
    elif e.get_label() is None:
        return "(%s)" % e.name
    else:
        return "**%s** (%s)" % (str(e.get_label()), e.name)


def py2rst(self, doctestfmt=False, fmt=None):
    """
    Return a textual representation of the given Python object as a
    reStructuredText bullet list.

    The Python object can be a layout, a layout element, an action or a
    database object.

    If it is an action, it must have parameters, and py2rst will render the
    params_layout.

    If it is a database object, you will get  a textual representation of a
    detail window on that object.

    If the optional argument `doctestfmt` is specified as `True`, then
    output contains less blank lines, which might be invalid
    reStructuredText but is more doctest-friendly.

    TODO: move this functionality to lino.api.doctests and rename it to
    something that reflects better what it does.

    """
    from lino.core.store import get_atomizer

    if isinstance(self, models.Model) and fmt is None:
        ar = self.get_default_table().request()
        def fmt(e):
            s = elem_label(e)
            if isinstance(e, FieldElement):
                sf = get_atomizer(self.__class__, e.field, e.field.name)
                getter = sf.full_value_from_object
                value = getter(self, ar)
                # value = e.value_from_object(self, None)
                if value is not None:
                    s += ": " + e.format_value(ar, value)
            return s

        dt = self.get_default_table()
        lh = dt.detail_layout.get_layout_handle()
        return py2rst(lh.main, doctestfmt, fmt)

    if isinstance(self, actions.Action):
        s = str(self)
        if self.params_layout:
            lh = self.params_layout.get_layout_handle(
                settings.SITE.kernel.default_ui)
            s += '\n'
            s += py2rst(lh.main, doctestfmt, fmt)
        return s


    if isinstance(self, BaseLayout):
        lh = self.get_layout_handle(settings.SITE.kernel.default_ui)
        return py2rst(lh.main, doctestfmt, fmt)

    if isinstance(self, Wrapper):
        self = self.wrapped

    if fmt is None:
        def fmt(e):
            s = elem_label(e)
            if visible_for(e) != visible_for(e.parent):
                s += " [visible for %s]" % visible_for(e)
            return s

    s = fmt(self)
    if isinstance(self, Container):
        use_ul = False
        for e in self.elements:
            if isinstance(e, Container):
                use_ul = True
        children = [py2rst(e, doctestfmt, fmt) for e in self.elements]
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
