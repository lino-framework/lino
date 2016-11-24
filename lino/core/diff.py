# Copyright 2010-2016 Luc Saffre
# License: BSD (see file COPYING for details)

import six
import difflib
from django.db.models.fields import NOT_PROVIDED
from django.db import models
from lino.core.signals import on_ui_updated
from lino.utils.xmlgen.html import E
from .utils import obj2str


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
        self.original_state = dict(watched.__dict__)
        self.watched = watched
        #~ self.is_new = is_new
        #~ self.request

    def get_updates(self, ignored_fields=frozenset(), watched_fields=None):
        """Yield a list of (fieldname, oldvalue, newvalue) tuples for each
        modified field. Optional argument `ignored_fields` can be a
        set of fieldnames to be ignored.

        """
        for k, old in self.original_state.items():
            if k not in ignored_fields:
                if watched_fields is None or k in watched_fields:
                    new = self.watched.__dict__.get(k, NOT_PROVIDED)
                    if old != new:
                        yield k, old, new

    def get_updates_html(self, *args, **kwargs):
        """A more descriptive variant of :meth:`get_updates` which uses a
        more intuitive description of the changes:

        - a unified diff for text fields.

        """
        for k, o, n in self.get_updates(*args, **kwargs):
            f = self.watched._meta.get_field(k)
            html = self.get_change_desc_html(f, o, n)
            if html:
                yield html
            # yield "{0} : {1}".format(k, desc)

    def get_change_desc_html(self, f, old, new):
        from lino.core.choicelists import ChoiceListField
        if isinstance(f, models.TextField):
            old = old or ''
            new = new or ''
            return E.li(
                E.b(f.verbose_name), " : ",
                E.pre('\n'.join(difflib.unified_diff(
                    old.splitlines(), new.splitlines(),
                    fromfile="before", tofile="after", lineterm=''))))
            
        if isinstance(f, models.DateTimeField):
            return
        if isinstance(f, models.ForeignKey):
            if old:
                old = f.rel.to.objects.get(pk=old)
            if new:
                new = f.rel.to.objects.get(pk=new)
        elif isinstance(f, ChoiceListField):
            if isinstance(old, six.string_types):
                old = f.choicelist.get_by_value(old)
            if isinstance(new, six.string_types):
                new = f.choicelist.get_by_value(new)
        else:
            old = obj2str(old)
            new = obj2str(new)
        return E.li(
            E.b(f.verbose_name), " : ",
            u"{0} --> {1}".format(old, new))
        
    def has_changed(self, fieldname):
        old = self.original_state[fieldname]
        if old != self.watched.__dict__.get(fieldname, NOT_PROVIDED):
            return True
        return False
        
    def is_dirty(self):
        #~ if self.is_new:
            #~ return True
        for k, v in self.original_state.items():
            if v != self.watched.__dict__.get(k, NOT_PROVIDED):
                return True
        return False

    def send_update(self, request):
        #~ print "ChangeWatcher.send_update()", self.watched
        on_ui_updated.send(
            sender=self.watched.__class__, watcher=self, request=request)


