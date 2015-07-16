# Copyright 2012-2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""Some diagnostic utilities."""

# from textwrap import fill
from atelier import rstgen

from django.conf import settings

from lino.core.layouts import BaseLayout
from lino.modlib.extjs.elems import Container, Wrapper, FieldElement
from lino.modlib.users.choicelists import UserProfiles


def get_window_actions():
    from lino.core.actors import actors_list
    # ui = settings.SITE.kernel.default_ui
    coll = dict()
    for a in actors_list:
        for ba in a.get_actions():
            if ba.action.is_window_action():
                wl = ba.get_window_layout() or ba.action.params_layout
                if wl is not None:
                    if isinstance(wl, basestring):
                        raise Exception("20150323 : {0}".format(ba))
                        # Was used to find Exception: 20150323 :
                        # <BoundAction(plausibility.Checkers,
                        # <ShowDetailAction detail (u'Detail')>)>

                    if not wl in coll:
                        # lh = wl.get_layout_handle(ui)
                        # for e in lh.main.walk():
                        #     e.loosen_requirements(a)
                        coll[wl] = ba
    return coll


def have_action(ba):
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
    if len(hidden) < len(visible):
        return "all except %s" % ', '.join(hidden)
    return ', '.join(visible)


def window_actions():
    # settings.SITE.startup()
    l = list(get_window_actions().values())

    def f(a, b):
        return cmp(a.full_name(), b.full_name())

    items = []
    for ba in sorted(l, f):
        items.append(
            "{0} (viewable for {1}) : {2}".format(
                ba.full_name(), have_action(ba), fields(ba)))

    return rstgen.ul(items)


def fields(ba):
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
    if have_action(self) != have_action(self.parent):
        s += " [visible for %s]" % have_action(self)
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


