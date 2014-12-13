# Copyright 2009-2014 Luc Saffre
# License: BSD (see file COPYING for details)
"""

.. autosummary::


"""

from django.conf import settings

from lino.utils import curry

from lino.core.frames import Frame

from lino.core.requests import VirtualRow
from lino.core import actions
from lino.core import fields

from lino.mixins.printable import (Printable, DirectPrintAction)
from lino.utils.xmlgen.html import E


class EmptyTableRow(VirtualRow, Printable):

    """
    Base class for virtual rows of an :class:`EmptyTable`.
    An EmptyTableRow instance
    """

    pk = -99998

    def __init__(self, table, **kw):
        self._table = table
        VirtualRow.__init__(self, **kw)

    def __unicode__(self):
        return unicode(self._table.label)

    def get_print_language(self):
        # same as Model.get_print_language
        return settings.SITE.DEFAULT_LANGUAGE.django_code

    def get_printable_context(self, **kw):
        # same as Model.get_printable_context
        kw = settings.SITE.get_printable_context(**kw)
        kw.update(this=self)  # preferred in new templates
        kw.update(language=self.get_print_language())
        return kw

    def get_template_groups(self):
        return [self._table.app_label + '/' + self._table.__name__]

    def filename_root(self):
        return self._table.app_label + '.' + self._table.__name__

    def __getattr__(self, name):
        """
        Since there is only one EmptyTableRow class, we simulate a
        getter here by manually creating an InstanceAction.
        """
        v = getattr(self._table, name)
        if isinstance(v, actions.Action):
            return actions.InstanceAction(v, self._table, self, None)
        # 20130525 dd.Report calls `get_story` on `self`, not on the `cls`
        if callable(v):
            return curry(v, self)
        #~ return v
        #~ raise Exception("")
        raise AttributeError(
            "EmptyTableRow on %s has no action and no callable '%s'" % (self._table, name))



class EmptyTable(Frame):

    #~ debug_permissions = True
    #~ has_navigator = False
    #~ hide_top_toolbar = True
    hide_navigator = True
    default_list_action_name = 'show'
    default_elem_action_name = 'show'

    do_print = DirectPrintAction()

    @classmethod
    def get_default_action(cls):
        return actions.ShowEmptyTable()

    @classmethod
    def create_instance(self, ar, **kw):
        if self.parameters:
            kw.update(ar.param_values)

        #~ for k,v in req.param_values.items():
            #~ kw[k] = v
        #~ for k,f in self.parameters.items():
            #~ kw[k] = f.value_from_object(None)
        obj = EmptyTableRow(self, **kw)
        kw = ar.ah.store.row2dict(ar, obj)
        obj._data = kw
        obj.update(**kw)
        return obj

    @classmethod
    def get_data_elem(self, name):
        de = super(EmptyTable, self).get_data_elem(name)
        if de is not None:
            return de
        a = name.split('.')
        if len(a) == 2:
            return getattr(getattr(settings.SITE.modules, a[0]), a[1])


class Report(EmptyTable):

    detail_layout = "body"

    report_items = NotImplementedError

    @classmethod
    def get_story(cls, self, ar):
        """Yield a sequence of story items. These can be (1)
        ElementTree elements or (2) AbstractTable or (3) action
        requests.

        """
        for A in cls.report_items:
            yield E.h2(unicode(A.label))
            if A.help_text:
                yield E.p(unicode(A.help_text))
            yield A

    @fields.virtualfield(fields.HtmlBox())
    def body(cls, self, ar):
        elems = tuple(ar.story2html(
            self.get_story(ar), master_instance=self))
        return E.div(*elems)

    @classmethod
    def as_appy_pod_xml(cls, self, apr):
        chunks = tuple(apr.story2odt(
            self.get_story(apr.ar), master_instance=self))
        return str('').join(chunks)  # must be utf8 encoded


