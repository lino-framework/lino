# Copyright 2010-2017 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

import difflib

from django.db.models.fields import NOT_PROVIDED
from django.db import models
from django.utils.translation import ugettext_lazy as _

from lino.core.signals import on_ui_updated
from etgen.html import E
# from .utils import obj2str
from .utils import obj2unicode

def state2dict(obj):
    d = {}
    for k, v in obj.__dict__.items():
        if not k.startswith('_'):
            d[k] = v
    # for fld in obj._meta.get_fields():
    #     # if isinstance(fld, VirtualField) and fld.editable:
    #     if isinstance(fld, VirtualField):
    #         v = NOT_PROVIDED
    #     else:
    #         v = obj.__dict__.get(fld.name, NOT_PROVIDED)
    #     d[fld.name] = v
    return d

class ChangeWatcher(object):
    """Lightweight volatile object to watch changes on a database object.

    This is used e.g. by the :data:`on_ui_updated
    <lino.core.signals.on_ui_updated>` signal.

    .. attribute:: watched

        The model instance which has been changed and caused the signal.

    .. attribute:: original_state

        a `dict` containing (fieldname --> value) before the change.

    """

    watched = None

    def __init__(self, watched):
        # self.original_state = dict(watched.__dict__)
        # self.original_state = {
        #     k:v for k, v in watched.__dict__.items()
        #     if not k.startswith('_')}
        self.original_state = state2dict(watched)
        self.watched = watched
        #~ self.is_new = is_new
        #~ self.request

    def get_updates(self, ignored_fields=frozenset(), watched_fields=None):
        """Yield a list of (fieldname, oldvalue, newvalue) tuples for each
        modified field. Optional argument `ignored_fields` can be a
        set of fieldnames to be ignored.

        """
        lst = []
        for k, new in state2dict(self.watched).items():
            if k not in ignored_fields:
                if watched_fields is None or k in watched_fields:
                    old = self.original_state.get(k, None)
                    if old != new:
                        lst.append((k, old, new))
        return sorted(lst, key=lambda x: x[0])

        # for k, old in self.original_state.items():
        #     if k not in ignored_fields:
        #         if watched_fields is None or k in watched_fields:
        #             new = self.watched.__dict__.get(k, NOT_PROVIDED)
        #             if old != new:
        #                 yield k, old, new

    def get_updates_html(self, *args, **kwargs):
        """A more descriptive variant of :meth:`get_updates` which uses a
        more intuitive description of the changes:

        - a unified diff for text fields.

        """
        for k, o, n in self.get_updates(*args, **kwargs):
            f = self.watched._meta.get_field(k)
            html = self.get_change_desc_html(f, o, n)
            if html is not None and len(html):
                yield html
            # yield "{0} : {1}".format(k, desc)

    def get_change_desc_html(self, f, old, new):
        from lino.core.choicelists import ChoiceListField
        if isinstance(f, models.TextField):
            old = old or ''
            new = new or ''
            if False:
                diff = difflib.unified_diff(
                    old.splitlines(), new.splitlines(),
                    fromfile="before", tofile="after", lineterm='')
                txt = E.pre('\n'.join(diff))
            else:
                labels = {
                    '+': _("lines added"),
                    '-': _("lines removed"),
                    '?': _("modifications"),
                    ' ': _("lines changed")}
                diff = list(difflib.ndiff(
                    old.splitlines(), new.splitlines()))
                counters = {}
                for ln in diff:
                    if ln:
                        k = ln[0]
                        c = counters.get(k, 0)
                        counters[k] = c + 1
                txt = ', '.join([
                    "{0} {1}".format(n, labels[op])
                    for op, n in counters.items()])
            return E.li(
                E.b(str(f.verbose_name)), " : ", txt)

        if isinstance(f, models.DateTimeField):
            return
        if isinstance(f, models.ForeignKey):
            if old:
                old = f.remote_field.model.objects.get(pk=old)
            if new:
                new = f.remote_field.model.objects.get(pk=new)
        elif isinstance(f, ChoiceListField):
            if isinstance(old, str):
                old = f.choicelist.get_by_value(old)
            if isinstance(new, str):
                new = f.choicelist.get_by_value(new)
        else:
            old = obj2unicode(old)
            new = obj2unicode(new)
        return E.li(
            E.b(str(f.verbose_name)), " : ",
            u"{0} --> {1}".format(old, new))

    def get_old_value(self, fieldname):
        """Return the old value of the specified field."""
        return self.original_state[fieldname]

    def has_changed(self, fieldname):
        """Return True if the specified field has changed."""
        old = self.original_state[fieldname]
        if old != self.watched.__dict__.get(fieldname, NOT_PROVIDED):
            return True
        return False

    def is_dirty(self):
        """Return True if any watched field has changed."""
        #~ if self.is_new:
            #~ return True
        for k, v in self.original_state.items():
            if v != self.watched.__dict__.get(k, NOT_PROVIDED):
                return True
        return False

    def send_update(self, request):
        #~ print "ChangeWatcher.send_update()", self.watched
        on_ui_updated.send(
            sender=self.watched.__class__, watcher=self,
            request=request)
