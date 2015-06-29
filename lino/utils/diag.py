# Copyright 2012-2015 Luc Saffre
# License: BSD (see file COPYING for details)

from textwrap import fill
from atelier import rstgen

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from lino.modlib.users.choicelists import UserProfiles


def get_window_actions():
    from lino.core.actors import actors_list
    ui = settings.SITE.kernel.default_ui
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
                        lh = wl.get_layout_handle(ui)
                        for e in lh.main.walk():
                            e.loosen_requirements(a)
                        coll[wl] = ba
    return coll


def have_action(ba):
    if ba is None:
        return _("N/A")
    visible = []
    hidden = []
    for p in UserProfiles.objects():
        name = p.name or p.value
        if ba.get_view_permission(p):
            visible.append(name)
        else:
            hidden.append(name)
    if len(hidden) == 0:
        return _("all")
    if len(visible) == 0:
        return _("nobody")
    if len(hidden) < len(visible):
        return _("all except %s") % ', '.join(hidden)
    return ', '.join(visible)


def window_actions():

    l = list(get_window_actions().values())

    def f(a, b):
        return cmp(a.full_name(), b.full_name())

    items = []
    for ba in sorted(l, f):
        items.append(
            "{0} (viewable for {1}) : ".format(
                ba.full_name(), have_action(ba), fields(ba)))

    return rstgen.ul(items)


def fields(ba):
    wl = ba.get_window_layout() or ba.action.params_layout
    if wl is None:
        return ''
    lh = wl.get_layout_handle(settings.SITE.kernel.default_ui)
    elems = [str(f.name) for f in lh._store_fields]
    return fill(' '.join(elems), 50)

