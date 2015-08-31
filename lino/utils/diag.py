# Copyright 2012-2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""Some diagnostic utilities."""

# from textwrap import fill
from atelier import rstgen

from django.conf import settings

from lino.core.layouts import BaseLayout
from lino.modlib.extjs.elems import Container, Wrapper, FieldElement
from lino.modlib.users.choicelists import UserProfiles
from lino.core import actors
from lino.core.utils import get_models
from lino.core.utils import full_model_name as fmn


class Analyzer(object):
    
    def __init__(self):
        self._initialized = False

    def analyze(self):
        if self._initialized:
            return
        self._initialized = True
        window_actions = dict()
        self.custom_actions = []
        for a in actors.actors_list:
            for ba in a.get_actions():
                if ba.action.is_window_action():
                    wl = ba.get_window_layout() or ba.action.params_layout
                    if wl is not None:
                        if isinstance(wl, basestring):
                            raise Exception("20150323 : {0}".format(ba))
                            # Was used to find Exception: 20150323 :
                            # <BoundAction(plausibility.Checkers,
                            # <ShowDetailAction detail (u'Detail')>)>

                        if not wl in window_actions:
                            # lh = wl.get_layout_handle(ui)
                            # for e in lh.main.walk():
                            #     e.loosen_requirements(a)
                            window_actions[wl] = ba
                else:  # if ba.action.custom_handler:
                    self.custom_actions.append(ba)
        l = list(window_actions.values())

        def f(a, b):
            return cmp(a.full_name(), b.full_name())
        self.window_actions = list(sorted(l, f))
        self.custom_actions = list(sorted(self.custom_actions, f))
    
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
    
    def show_action_permissions(self, *classes):
        self.analyze()
        items = []
        for ba in analyzer.custom_actions + analyzer.window_actions:
            if isinstance(ba.action, classes):
                items.append(
                    "{0} : visible for {1}".format(
                        ba.full_name(), visible_for(ba)))

        return rstgen.ul(items)
    
    def show_foreign_keys(self):
        self.analyze()
        tdp = dict()  # target model -> delete handler -> pointer list
        for target in get_models():
            dp = tdp.setdefault(target, dict())
            for m, fk in target._lino_ddh.fklist:
                k = fk.rel.on_delete
                p = dp.setdefault(k, [])
                p.append((m, fk))

        def fk2str(mfk):
            return "{0}.{1}".format(fmn(mfk[0]), mfk[1].name)

        items1 = []
        for target, dp in tdp.items():
            items2 = []
            for dh, pl in dp.items():
                items2.append(
                    "{0} : {1}".format(
                        dh.__name__, ', '.join([fk2str(mfk) for mfk in pl])))
            if len(items2):
                items2 = sorted(items2)
                items1.append("{0} :\n{1}".format(
                    fmn(target), rstgen.ul(items2)))
    
        items1 = sorted(items1)
        return rstgen.ul(items1)
    
analyzer = Analyzer()


def visible_for(ba):
    """Shows a list of user profiles for which this action is visible."""
    if ba is None:
        return "N/A"
    visible = []
    hidden = []
    for p in UserProfiles.objects():
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

    Where "any" actually means a layout or a layout element.
    :class:`lino.core.layouts.BaseLayout`
    :mod:`lino.modlib.extjs.elems`

    If the optional argument `doctestfmt` is specified as `True`, then
    output contains less blank lines which might be invalid
    reStructuredText but is more doctest-friendly.

    """
    if isinstance(self, BaseLayout):
        lh = self.get_layout_handle(settings.SITE.kernel.default_ui)
        return py2rst(lh.main, doctestfmt)
        
    if isinstance(self, Wrapper):
        self = self.wrapped

    if isinstance(self, FieldElement):
        s = "**%s** (%s)" % (unicode(self.field.verbose_name), self.field.name)
    elif self.label is None:
        s = "(%s)" % self.name
    else:
        s = "**%s** (%s)" % (unicode(self.label), self.name)
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


