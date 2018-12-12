# Copyright 2009-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""See :doc:`/dev/layouts/index`.

"""

from __future__ import unicode_literals
from builtins import str
from builtins import object
import six
import logging ; logger = logging.getLogger(__name__)
import re

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db.models.fields import NOT_PROVIDED
from django.db.models.fields.related import ForeignObject
# from django.contrib.contenttypes.fields import GenericRelation

from lino.core import constants
from lino.core.fields import fields_list, VirtualField, wildcard_data_elems
from lino.core.plugin import Plugin


class LayoutError(RuntimeError):
    pass

LABEL_ALIGN_TOP = 'top'
LABEL_ALIGN_LEFT = 'left'
LABEL_ALIGN_RIGHT = 'right'

ALLOW_DUPLICATE_ELEMS = True


def DEBUG_LAYOUTS(lo):
    #~ if lo._table.__name__ == 'Users':
        #~ return True
    return False


class DummyPanel(object):
    """
    A layout panel which does not exist in the current configuration
    but might exist as a real panel in some other configuration.
    """
    pass


class Panel(object):

    """
    To be used when a panel cannot be expressed using a simple
    template string because it requires one or more options. These
    `options` parameters can be:

    - label
    - required_roles
    - window_size
    - label_align

    Unlike a :class:`BaseLayout` it cannot have any child panels
    and cannot become a tabbed panel.
    """

    def __init__(self, desc, label=None, **options):
        # assert not 'required' in options
        self.desc = desc
        if label is not None:
            options.update(label=label)
        self.options = options

    def replace(self, *args, **kw):
        """
        Calls the standard :meth:`string.replace`
        method on this Panel's template.
        """
        self.desc = self.desc.replace(*args, **kw)



class LayoutHandle(object):
    """
    A `LayoutHandle` analyzes an instance of :class:`BaseLayout` or a some
    subclass thereof and holds the resulting metadata, especially the layout
    elements and panels provided by the renderer.

    The implementation of layout elements is left to the ui renderer,
    but we differentiate *panels* from *atomic elements*. A panel is a
    group of elements and is either *vertical* or *horizontal*.

    LayoutHandle is not meant to be subclassed. The same class is used
    for all kinds of BaseLayout instances.

    .. attribute:: main

        The main element.
    """

    def __init__(self, layout, ui):
        assert isinstance(layout, BaseLayout)
        assert isinstance(ui, Plugin)
        self.layout = layout
        self.ui = ui
        self.hidden_elements = layout.hidden_elements
        self._store_fields = []
        self._names = {}

        # self.define_panel('main', layout.main)
        if settings.SITE.mobile_view:
            main = layout.main_m or layout.main
        else:
            main = layout.main
        self.define_panel('main', main)

        self.main = self._names.get('main')
        if self.main is None:
            raise Exception(
                "Failed to create main element %r for %s." % (
                    layout.main, layout))

        self.width = self.main.width
        self.height = self.main.height

        self.layout.setup_handle(self)
        for k, v in self.layout._labels.items():
            if k not in self._names:
                raise Exception(
                    "%s has no attribute %r (layout.main is %r)" %
                    (self, k, layout.main))
            self._names[k].set_label(v)

    def desc2elem(self, elemname, desc, **kwargs):
        # logger.debug("desc2elem(panelclass,%r,%r)",elemname,desc)

        if isinstance(desc, DummyPanel):
            return None

        if isinstance(desc, Panel):
            if len(kwargs):
                newkw = dict(desc.options)
                newkw.update(kwargs)
                kwargs = newkw
            else:
                kwargs = desc.options
            desc = desc.desc
            # if 'label_align' in kwargs:
            #     print("20170921 desc2elem", elemname, desc, kwargs)

        if not isinstance(desc, six.string_types):
            raise Exception("{} is {} (must be a string)".format(
                elemname, desc))

        # flatten continued lines:
        desc = desc.replace('\\\n', '')

        # expand aliases (configurable fields)
        for alias, repl in self.layout._datasource.get_layout_aliases():
            desc = re.sub(r"\b"+alias+r"\b", repl, desc)

        # expand wildcards
        if '*' in desc:
            assert elemname == 'main'
            explicit_specs = set()
            remote_wildcards = []
            for spec in desc.split():
                if '*' not in spec:
                    name, kwargs = self.splitdesc(spec)
                    # if 'hide_sum' in kwargs:
                    #     raise Exception("20180210a")
                    explicit_specs.add(name)
                elif len(spec) > 1:
                    remote_wildcards.append(spec)
                    
            for rwspec in remote_wildcards:
                assert rwspec.endswith('__*')
                rmodel = rwspec[:-3]
                rwprefix = rwspec[:-1]

                fld = self.get_data_elem(rmodel)
                if fld is None:
                    raise Exception(
                        "Invalid remote wildcard %s" % rw)
                rwmodel = fld.remote_field.model
                rwnames = []
                for de in wildcard_data_elems(rwmodel):
                    if isinstance(de, (VirtualField, ForeignObject)):
                        continue
                    if self.use_as_wildcard(de):
                        k = rwprefix + de.name
                        if k not in explicit_specs:
                            rwnames.append(k)
                            self.hidden_elements.add(k)
                wildcard_str = self.layout.join_str.join(rwnames)
                # print("20180112a", rwmodel, wildcard_str)
                # print("20180112b", rwspec, desc)
                desc = desc.replace(rwspec, wildcard_str)

            wildcard_names = []
            for de in self.layout._datasource.wildcard_data_elems():
                if de.name not in explicit_specs:
                    if self.use_as_wildcard(de):
                        wildcard_names.append(de.name)
                        if len(explicit_specs) or isinstance(de, VirtualField):
                            self.hidden_elements.add(de.name)
            wildcard_str = self.layout.join_str.join(wildcard_names)
            desc = desc.replace('*', wildcard_str)

            mk = self.layout._datasource.master_key
            if mk and mk not in explicit_specs \
               and mk not in self.hidden_elements:
                desc += ' ' + mk
                self.hidden_elements.add(mk)

        if "\n" in desc:
            # it's a vertical box
            vertical = True
            
            # To get a hbox, the template string must not contain any
            # newline.

            elems = []
            i = 0
            for x in desc.splitlines():
                x = x.strip()
                if len(x) > 0 and not x.startswith("# "):
                    i += 1
                    e = self.desc2elem(elemname + '_' + str(i), x)
                    if e is not None:
                        elems.append(e)
        else:
            # it's a horizontal box
            vertical = False
            elems = []
            for x in desc.split():
                if not x.startswith("#"):
                    # 20100214 pcsw.PersonDetail hatte 2 MainPanels,
                    # weil PageLayout kein einzeiliges (horizontales)
                    # `main` vertrug
                    e = self.create_element(x)
                    if e is None:
                        pass
                    elif isinstance(e, list):
                        elems += e
                    else:
                        elems.append(e)
        if len(elems) == 0:
            return None
        if len(elems) == 1 and elemname != 'main':
            elems[0].setup(**kwargs)
            return elems[0]
        from lino.core.elems import create_layout_panel
        return create_layout_panel(
            self, elemname, vertical, elems, **kwargs)

    def define_panel(self, name, desc, **kw):
        if not desc:
            return
        if name in self._names:
            if ALLOW_DUPLICATE_ELEMS:
                return self._names[name]
            else:
                raise Exception(
                    'Duplicate element definition %s = %r in %s'
                    % (name, desc, self.layout))
        e = self.desc2elem(name, desc, **kw)
        if e is None:
            return
        self._names[name] = e
        return e

    def create_element(self, desc_name):
        from lino.core.elems import create_layout_element
        #~ logger.debug("create_element(%r)", desc_name)
        name, options = self.splitdesc(desc_name)
        # if 'hide_sum' in options:
        #     raise Exception("20180210b")
        if name in self._names:
            if ALLOW_DUPLICATE_ELEMS:
                return self._names[name]
            else:
                raise Exception(
                    'Duplicate element usage %s = %r in %s'
                    % (name, desc_name, self.layout))
        desc = getattr(self.layout, name, None)
        if desc is not None:
            return self.define_panel(name, desc, **options)
        e = create_layout_element(self, name, **options)
        if e is None:
            return None  # e.g. NullField
        if name in self.hidden_elements:
            # 20150216 hidden formpanel fields
            # if isinstance(self.layout, FormLayout):
            #     return None
            if isinstance(e, list):  # it is a babelfield
                for be in e:
                    be.hidden = True
            else:
                e.hidden = True
        
        self.ui.setup_layout_element(e)
        self.layout.setup_element(self, e)
        self._names[name] = e
        return e

    def splitdesc(self, picture, **options):
        """Parse the given element descriptor and return a tuple `(name,
        options)` where `name` is the element name and `options` is a
        `dict` with keyword arguments to be forwarded to the widget
        constructor (:class:`LayoutElement`).

        """
        a = picture.split(":", 1)
        if len(a) == 1:
            name = picture
        elif len(a) == 2:
            name = a[0]
            a = a[1].split("x", 1)
            if len(a) == 1:
                options.update(width=int(a[0]))
            elif len(a) == 2:
                options.update(width=int(a[0]), height=int(a[1]))
            else:
                raise Exception("Invalid picture '%s'" % picture)
        else:
            raise Exception("Invalid picture '%s'" % picture)

        options = self.layout._datasource.get_widget_options(name, **options)
        return name, options

    def __str__(self):
        return "%s for %s" % (self.__class__.__name__, self.layout)

    def __getitem__(self, name):
        return self._names[name]

    def add_store_field(self, field):
        self._store_fields.append(field)

    def get_title(self, ar):
        return self.layout.get_title(ar)

    def walk(self):
        return self.main.walk()

    def ext_lines(self, request):
        return self.main.ext_lines(request)

    def use_as_wildcard(self, de):
        if de.name.endswith('_ptr'):
            return False
        # if isinstance(de, VirtualField):
        #     return False
        if isinstance(self.layout, ColumnsLayout):
            if de.name == self.layout._datasource.master_key:
                return False
        return True

    def get_data_elem(self, name):
        # 20150610 : data elements defined on the layout have
        # precedence over those defined in the datasource.

        # if not name in ('__str__', '__unicode__', 'name', 'label'):
        if name not in ('name', 'label'):
            value = getattr(self.layout, name, NOT_PROVIDED)
            # if name == 'ledger':
            #     logger.info("20150610 'ledger' in instance of %s is %r",
            #                 self.layout.__class__, value)
            if value is not NOT_PROVIDED:
                return value
        return self.layout.get_data_elem(name)

    def get_choices_url(self, *args, **kw):
        return self.layout.get_choices_url(
            settings.SITE.kernel.default_renderer.plugin,
            *args, **kw)


class BaseLayout(object):
    """
    Base class for all Layouts (:class:`FormLayout`, :class:`ColumnsLayout`
    and  :class:`ParamsLayout`).

    A Layout instance just holds the string templates.
    It is designed to be subclassed by applications programmers.


    In some cases we still use the (reprecated)  methods
    :meth:`set_detail_layout <lino.core.actors.Actor.set_detail_layout>`,
    :meth:`set_insert_layout <lino.core.actors.Actor.set_insert_layout>`,
    :meth:`add_detail_panel <lino.core.actors.Actor.add_detail_panel>`
    and
    :meth:`add_detail_tab <lino.core.actors.Actor.add_detail_tab>`
    on the :class:`Actor <lino.core.actors.Actor>`.

    """

    _datasource = None
    required_roles = None
    label_align = LABEL_ALIGN_TOP

    window_size = None
    """A tuple `(width, height)` that specifies the size of the window to
    be used for this layout.

    For example, specifying `window_size=(50, 30)` means "50
    characters wide and 30 lines high".  The `height` value can also
    be the string ``'auto'``.

    """

    editable = True
    """Lino sets this to False for layouts on a non-editable actor.

    """
    
    main = None
    """The description of the main element of this layout.

    For a :class:`ColumnsLayout` this is the same as
    :attr:`column_names
    <lino.core.tables.AbstractTable.column_names>`.

    """
    
    main_m = None
    """An optional alternative for :attr:`main` to use when
    :attr:`mobile_view <lino.core.site.Site.mobile_view>` is True.

    """

    def __init__(self, main=None, datasource=None,
                 hidden_elements=None, **kw):
        """
        datasource is either an actor or an action.
        """
        self._labels = self.override_labels()
        self._added_panels = dict()
        self._other_datasources = set()
        self.hidden_elements = hidden_elements or set()
        self._element_options = dict()
        if main is not None:
            self.main = main
        #~ elif not hasattr(self,'main'):
        elif self.main is None:
            raise Exception(
                "Cannot instantiate %s without `main`." % self.__class__)
        self.set_datasource(datasource)
        for k, v in kw.items():
            # The following test is deactivated because it is possible
            # to dynamically define subpanels on a panel,
            # e.g. MergeAction.keep_volatiles
            
            # if not hasattr(self, k):
            #     raise Exception("Got unexpected keyword %s=%r" % (k,v))
            setattr(self, k, v)

        # if "Sign in" in str(datasource):
        #     # if self.label_align == 'left':
        #     print("20170921 BaseLayout.__init__", self.label_align)

    def __str__(self):
        return "{}.{} on {!r}".format(
            self.__class__.__module__, self.__class__.__name__,
            self._datasource)

    def set_datasource(self, ds):
        self._datasource = ds
        if ds is not None:
            if isinstance(self.hidden_elements, six.string_types):
                self.hidden_elements = set(fields_list(
                    ds, self.hidden_elements))
            self.hidden_elements |= ds.hidden_elements
            self.editable = ds.editable
            #~ if str(ds).endswith('Partners'):
                #~ print "20130124 set_datasource ", self,self.hidden_elements

    def get_chooser_holder(self):
        return self._datasource

    def override_labels(self):
        return dict()

    def get_data_elem(self, name):
        return self._datasource.get_data_elem(name)

    def remove_element(self, *args):
        """
        Removes specified element names from this layout's `main` template.
        """
        for name in args:
            self.main = self.main.replace(name, '')

    def setup_handle(self, lh):
        pass

    def setup_element(self, lh, e):
        pass

    def update(self, **kw):
        """Update the template of one or more panels.

        """
        for k, v in list(kw.items()):
            if DEBUG_LAYOUTS(self):
                msg = """\
In %s, updating attribute %r:
--- before:
%s
--- after:
%s
---""" % (self, k, getattr(self, k, '(undefined)'), v)
                logger.info(msg)
            setattr(self, k, v)

    def add_panel(self, name, tpl, label=None, **options):
        """
        Adds a new panel to this layout.

        Arguments:

        - `name` is the internal name of the panel
        - `tpl` the template string
        - `label` an optional label
        - any further keyword are passed as options to the new panel
        """
        #~ if hasattr(self,'_extjs3_handle'):
            #~ raise Exception("Cannot update for layout after UI has been set up.")
        if '\n' in name:
            raise Exception("name may not contain any newline")
        if ' ' in name:
            raise Exception("name may not contain any whitespace")
        #~ if getattr(self,name,None) is not None:
            #~ raise Exception("name %r already defined in %s" % (name,self))
        self._add_panel(name, tpl, label, options)

    def _add_panel(self, name, tpl, label, options):
        if tpl is None:
            return  # when does this occur?
        if hasattr(self, name):
            raise Exception("Oops, %s has already a name %r" % (self, name))
        if DEBUG_LAYOUTS(self):
            msg = """\
Adding panel %r to %s ---:
%s
---""" % (name, self, tpl)
            logger.info(msg)
        setattr(self, name, tpl)
        self._added_panels[name] = tpl  # 20120914c
        if label is not None:
            self._labels[name] = label
        if options:
            self._element_options[name] = options

    def add_tabpanel(self, name, tpl=None, label=None, **options):
        """
        Add a tab panel to an existing layout.
        Arguments: see :meth:`BaseLayout.add_panel`.
        The difference with :meth:`BaseLayout.add_panel`
        is that this potentially turns the existing `main` panel to a tabbed panel.

        Arguments:

        - `name` is the internal name of the panel
        - `tpl` the template string
        - `label` an optional label
        """
        #~ print "20120526 add_detail_tab", self, name
        #~ if hasattr(self,'_extjs3_handle'):
            #~ raise Exception("Cannot update form layout after UI has been set up.")
        if '\n' in name:
            raise Exception("name may not contain any newline")
        if ' ' in name:
            raise Exception("name may not contain any whitespace")
        if '\n' in self.main:
            if hasattr(self, 'general'):
                raise NotImplementedError("""\
%s has both a vertical `main` and a panel called `general`.""" % self)
            self.general = self.main
            self.main = "general " + name
            self._labels['general'] = _("General")
            if DEBUG_LAYOUTS(self):
                msg = """\
add_tabpanel() on %s moving content of vertical 'main' panel to 'general'.
New 'main' panel is %r"""
                logger.info(msg, self, self.main)
        else:
            self.main += " " + name
            if DEBUG_LAYOUTS(self):
                msg = """\
add_tabpanel() on %s horizontal 'main' panel %r."""
                logger.info(msg, self, self.main)
        #~ if tpl is not None:
        self._add_panel(name, tpl, label, options)
            #~ self._add_panel(name,tpl)
            #~ setattr(self,name,tpl)
            # ~ self._added_panels[name] = tpl # 20120914c
        #~ if label is not None:
            #~ self._labels[name] = label
        #~ self._element_options[name] = options
        #~ if kw:
            #~ print 20120525, self, self.detail_layout._element_options

    def get_layout_handle(self, ui=None):
        """
        `ui` is a :class:`Plugin` instance.
        """
        if ui is None:
            ui = settings.SITE.kernel.default_ui
        hname = ui.ui_handle_attr_name
        if hname is None:
            raise Exception(
                "{0} has no `ui_handle_attr_name`!".format(ui))

        # we do not want any inherited handle
        h = self.__dict__.get(hname, None)
        if h is None:
            # if str(self._datasource) == 'courses.Pupils':
            # print("20160329 layouts.py make handle", self._datasource)
            h = LayoutHandle(self, ui)
            setattr(self, hname, h)
        return h

    def get_choices_url(self, ui, field, **kw):
        # 20140101
        # return settings.SITE.build_admin_url(
        #     "choices",
        #     self._datasource.app_label,
        #     self._datasource.__name__,
        #     field.name, **kw)

        return ui.build_plain_url(
            "choices",
            self._datasource.app_label,
            self._datasource.__name__,
            field.name, **kw)

    def to_rst(self, user_type=None, name=None):
        lh = self.get_layout_handle(settings.SITE.kernel.default_ui)
        # if user_type is None:
        #     user_type = UserTypes.admin
        if name is None:
            e = lh.main
        else:
            e = lh.main.find_by_name(name)
        return e.to_rst(user_type)

    def __getitem__(self, name):
        """
        Used for writing doctests. Untested example:

        >>> print(py2rst(pcsw.Clients.detail_layout['calendar']))
        **Calendar** (calendar) [visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin 910]:
        - **Calendar entries** (cal.EntriesByClient)
        - **Tasks** (cal.TasksByProject) [visible for 100 110 120 200 300 400 410 500 510 admin 910]
        <BLANKLINE>


        """
        lh = self.get_layout_handle(settings.SITE.kernel.default_ui)
        return lh[name]


class FieldLayout(BaseLayout):
    pass


class FormLayout(FieldLayout):
    """Base class for layout descriptions of detail and insert windows.

    Lino instantiates this for every :attr:`detail_layout
    <lino.core.actors.Actor.detail_layout>` and for every
    :attr:`insert_layout <lino.core.actors.Actor.insert_layout>`.

    """
    join_str = "\n"


class DetailLayout(FormLayout):
    pass


class InsertLayout(FormLayout):
    pass


class ColumnsLayout(FieldLayout):
    """
    A layout for describing the columns of a table.

    Lino automatically creates one instance of this for every table
    using the string specified in that table's :attr:`column_names
    <lino.core.tables.AbstractTable.column_names>` attribute.
    
    """
    join_str = " "

    def set_datasource(self, ds):
        if ds is None:
            raise Exception("20130327 No datasource for %r" % self)
        super(ColumnsLayout, self).set_datasource(ds)


class ParamsLayout(BaseLayout):
    """
    A Layout description for a table parameter panel.

    Lino instantiates this for every actor with
    :attr:`parameters <lino.core.actors.Actor.parameters>`,
    based on that actor's
    :attr:`params_layout <lino.core.actors.Actor.params_layout>`.
    """
    join_str = " "
    url_param_name = constants.URL_PARAM_PARAM_VALUES
    params_store = None

    def get_data_elem(self, name):
        de = self._datasource.get_param_elem(name)
        if de is None:
            de = self._datasource.get_data_elem(name)
        return de

    def setup_handle(self, lh):
        # if str(self._datasource) == 'courses.Pupils':
        #     print("20160329 setup_handle")
        from lino.core.store import ParameterStore
        self.params_store = ParameterStore(lh, self.url_param_name)


class ActionParamsLayout(ParamsLayout):
    """
    A Layout description for an action parameter panel.

    Lino instantiates this for every :attr:`params_layout
    <lino.core.actions.Action.params_layout>` of a custom action.

    A subclass of :class:`ParamsLayout`.
    """
    join_str = "\n"
    window_size = (50, 'auto')
    url_param_name = constants.URL_PARAM_FIELD_VALUES

    def setup_element(self, lh, e):
        from lino.utils import jsgen
        e.declare_type = jsgen.DECLARE_THIS

    def get_choices_url(self, ui, field, **kw):
        return settings.SITE.kernel.default_ui.build_plain_url(
            "apchoices",
            self._datasource.defining_actor.app_label,
            self._datasource.defining_actor.__name__,
            self._datasource.action_name,
            field.name, **kw)



