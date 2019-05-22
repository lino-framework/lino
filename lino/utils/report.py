# Copyright 2009-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
"""


"""
from __future__ import unicode_literals, print_function
from builtins import str

from django.conf import settings

from lino.utils import curry

from lino.core.frames import Frame

from lino.core.requests import InstanceAction
from lino.core.requests import VirtualRow
from lino.core.actions import ShowEmptyTable, Action
from lino.core import fields

from lino.modlib.printing.mixins import Printable
from lino.modlib.printing.mixins import DirectPrintAction
# from lino.modlib.printing.choicelists import SimpleBuildMethod
from etgen.html import E


from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class EmptyTableRow(VirtualRow, Printable):
    """
    Base class for virtual rows of an :class:`EmptyTable`.
    An EmptyTableRow instance
    """

    class Meta(object):
        abstract = True

    pk = -99998

    def __init__(self, table, **kw):
        self._table = table
        VirtualRow.__init__(self, **kw)

    def __str__(self):
        return str(self._table.label)

    def before_printable_build(self, bm):
        pass

    def filename_root(self):
        return self._table.app_label + '.' + self._table.__name__

    # def get_print_language(self):
    #     # same as Printable.get_print_language
    #     return settings.SITE.DEFAULT_LANGUAGE.django_code

    # def get_printable_context(self, ar=None, **kw):
    #     # same as Model.get_printable_context
    #     kw = ar.get_printable_context(**kw)
    #     kw.update(this=self)  # preferred in new templates
    #     kw.update(language=self.get_print_language() \
    #               or settings.SITE.DEFAULT_LANGUAGE.django_code)
    #     return kw

    def get_template_groups(self):
        return self._table.get_template_groups()

    def get_print_templates(self, *args):
        """Overrides
        :meth:`lino.modlib.printing.mixins.Printable.get_print_templates`

        """
        return self._table.get_print_templates(*args)

    def get_build_method(self):
        return self._table.build_method \
            or super(EmptyTableRow, self).get_build_method()

    def get_build_options(self, bm, **opts):
        # header_center
        return self._table.get_build_options(bm, **opts)

    def get_subtitle(self, ar):
        
        return ', '.join(self._table.get_title_tags(ar))
        
    def __getattr__(self, name):
        """
        Since there is only one EmptyTableRow class, we simulate a
        getter here by manually creating an InstanceAction.
        """
        # if name not in ('get_story'):
        #     raise Exception("20170910 %s" % name)
        v = getattr(self._table, name)
        if isinstance(v, Action):
            return InstanceAction(v, self._table, self, None)
        # 20130525 dd.Report calls `get_story` on `self`, not on the `cls`
        if callable(v):
            return curry(v, self)
        #~ return v
        #~ raise Exception("")
        raise AttributeError(
            "EmptyTableRow on %s has no action and no callable '%s'" % (
                self._table, name))


class EmptyTable(Frame):
    """
    A "Table" that has exactly one virtual row and thus is visible
    only using a Detail view on that row.

    Subclassed by :class:`lino.modlib.about.About` and
    :class:`Report`.
    """

    #~ debug_permissions = True
    #~ has_navigator = False
    #~ hide_top_toolbar = True
    abstract = True
    hide_navigator = True
    default_list_action_name = 'show'
    default_elem_action_name = 'show'

    build_method = None

    @classmethod
    def get_default_action(cls):
        return ShowEmptyTable(cls.detail_layout)

    @classmethod
    def get_template_groups(self):
        return [self.app_label + '/' + self.__name__]

    @classmethod
    def get_print_templates(self, bm, action):
        """Called from EmptyTableRow. """
        return [bm.get_default_template(self)]

    @classmethod
    def get_build_options(self, bm, **opts):
        return opts

    @classmethod
    def create_instance(self, ar, **kw):
        if self.parameters:
            kw.update(ar.param_values)

        obj = EmptyTableRow(self, **kw)
        kw = ar.ah.store.row2dict(ar, obj)
        obj._data = kw
        obj.update(**kw)
        return obj

    @classmethod
    def wildcard_data_elems(self):
        return self.parameters.values()
        
    @classmethod
    def get_data_elem(self, name):
        de = super(EmptyTable, self).get_data_elem(name)
        if de is not None:
            return de
        de = self.parameters.get(name, None)
        if de is not None:
            return de
        a = name.split('.')
        if len(a) == 2:
            return getattr(getattr(settings.SITE.models, a[0]), a[1])


class Report(EmptyTable):
    """

    A special kind of :class:`EmptyTable` used to create "reports".  A report
    is a series of headings, paragraphs and tables combined into a single
    printable and previewable document.

    When subclassing this, application code must either define
    :attr:`report_items` or implement an alternative :meth:`get_story`.

    Usage examples:
    :class:`lino_xl.lib.courses.StatusReport`
    :class:`lino_xl.lib.ledger.Situation`
    :class:`lino_xl.lib.ledger.ActivityReport`
    :class:`lino_welfare.modlib.integ.ActivityReport`

    Note that there is also :class:`lino.modlib.users.UserPlan` and
    :class:`lino.mixins.Story` for more expensive "reports" where you use
    cached data :class:`lino_xl.lib.sheets.Report`.

    """

    detail_layout = "body"
    abstract = True

    do_print = DirectPrintAction()
    # go_button = ExplicitRefresh()

    report_items = None
    """ """

    # @classmethod
    # def request(self, **kw):
    #     """Return an action request on this actor.

    #     """
    #     kw.update(actor=self)
    #     return ActionRequest(**kw)

    @classmethod
    def get_template_groups(self):
        return ['report', self.app_label + '/' + self.__name__]

    # @classmethod
    # def get_print_templates(self, bm, action):
    #     """Called from EmptyTableRow.
    #     Overrides
    #     :meth:`lino.modlib.printing.mixins.Printable.get_print_templates`

    #     """
    #     if isinstance(bm, SimpleBuildMethod):
    #         return ['Report'+bm.template_ext]
    #         return [bm.get_default_template(self)]
    #     return ['Report'+bm.template_ext, bm.get_default_template(self)]

    @classmethod
    def get_build_options(self, bm, **opts):
        if bm.templates_name == 'wk':
            opts['footer-left'] = "<p>Footer [page]</p>"
        return opts

    # @classmethod
    # def get_title_base(self, ar):
    #     return self.title or self.label

    @classmethod
    def get_title(self, ar):
        return self.title or self.label

    @fields.virtualfield(fields.HtmlBox())
    def body(cls, self, ar):
        ar.master_instance = self
        return ar.story2html(self.get_story(ar))

    @classmethod
    def as_appy_pod_xml(cls, self, apr):
        chunks = tuple(apr.story2odt(
            self.get_story(apr.ar), master_instance=self))
        return str('').join(chunks)  # must be utf8 encoded

    @classmethod
    def get_story(cls, self, ar):
        """
        Yield a sequence of story items. Every item can be (1) an
        ElementTree element or (2) a table or (3) an action request.
        """
        # cls.check_params(cls.param_values)
        if cls.report_items is None:
            raise Exception("{0} has no report_items".format(cls))
        for A in cls.report_items:
            yield E.h2(str(A.label))
            # if A.help_text:
            #     yield E.p(str(A.help_text))
            yield A

    @classmethod
    def to_rst(self, ar, column_names=None, **kwargs):
        raise Exception("To be replaced by rt.show()")
        # obj = self.create_instance(ar)
        # return """\
        # .. raw:: html
        
        #    %s
        # """ % tostring(obj.body).replace('\n', ' ')
