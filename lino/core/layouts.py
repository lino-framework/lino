# Copyright 2009-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"See :doc:`/dev/layouts`."

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db.models.fields import NOT_PROVIDED
from django.db.models.fields.related import SingleRelatedObjectDescriptor
from django.contrib.contenttypes import generic

# from lino.utils.xmlgen.html import E

from lino.core import constants
from lino.core.fields import fields_list


class LayoutError(RuntimeError):
    pass

LABEL_ALIGN_TOP = 'top'
LABEL_ALIGN_LEFT = 'left'
LABEL_ALIGN_RIGHT = 'right'


def DEBUG_LAYOUTS(lo):
    #~ if lo._table.__name__ == 'Users':
        #~ return True
    return False


class Panel(object):

    """
    This is available as `dd.Panel`.
    Used when a panel is more complex than what can be expressed
    using a simple template string.

    The `options` parameter can be:

    - label
    - required

    Unlike a :class:`FormPanel` it cannot have any child panels
    and cannot become a tabbed panel.
    """

    def __init__(self, desc, label=None, **options):
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

    #~ def remove_element(self,*args):
        #~ """
        #~ Removes specified element names from this Panel's `main` template.
        #~ """
        #~ for name in args:
            #~ if not name in self.desc:
                #~ raise Exception("Panel has no element '%s'" % name)
            #~ self.desc = self.desc.replace(name,'')


class LayoutHandle:
    """
    A `LayoutHandle` analyzes some subclass of :class:`BaseLayout` and
    stores the resulting LayoutElements provided by the UI.

    The same class is used for all kinds of BaseLayout instances.
    """

    def __init__(self, layout):
        assert isinstance(layout, BaseLayout)
        self.layout = layout
        self.hidden_elements = layout.hidden_elements
        self._store_fields = []
        self._names = {}

        self.define_panel('main', layout.main)

        self.main = self._names.get('main')
        if self.main is None:
            raise Exception(
                "Failed to create main element %r for %s." % (
                    layout.main, layout))

        self.width = self.main.width
        self.height = self.main.height

        self.layout.setup_handle(self)
        for k, v in self.layout._labels.items():
            if not k in self._names:
                raise Exception(
                    "%s has no attribute %r (layout.main is %r)" %
                    (self, k, layout.main))
            self._names[k].label = v

    def __str__(self):
        return "%s for %s" % (self.__class__.__name__, self.layout)

    def add_store_field(self, field):
        self._store_fields.append(field)

    def get_title(self, ar):
        return self.layout.get_title(ar)

    def walk(self):
        return self.main.walk()

    def ext_lines(self, request):
        return self.main.ext_lines(request)

    def desc2elem(self, elemname, desc, **kw):
        # logger.debug("desc2elem(panelclass,%r,%r)",elemname,desc)

        if isinstance(desc, Panel):
            if len(kw):
                newkw = dict(desc.options)
                newkw.update(kw)
                kw = newkw
            else:
                kw = desc.options
            desc = desc.desc

        # flatten continued lines:
        desc = desc.replace('\\\n', '')

        if '*' in desc:
            assert elemname == 'main'
            explicit_specs = set()
            for spec in desc.split():
                if spec != '*':
                    name, kw = self.splitdesc(spec)
                    explicit_specs.add(name)
            wildcard_names = [de.name for de in
                              self.layout._datasource.wildcard_data_elems()
                              if (de.name not in explicit_specs)
                              and self.use_as_wildcard(de)]
            wildcard_str = self.layout.join_str.join(wildcard_names)
            desc = desc.replace('*', wildcard_str)
            if len(explicit_specs) > 0:
                self.hidden_elements = self.hidden_elements | set(
                    wildcard_names)

        if "\n" in desc:
            # it's a vertical box
            vertical = True
            """To get a hbox, the template string may not contain any newline.
            """
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
            elems[0].setup(**kw)
            return elems[0]
        e = create_layout_panel(self, elemname, vertical, elems, **kw)
        return e

    def define_panel(self, name, desc, **kw):
        if not desc:
            return
        if name in self._names:
            raise Exception(
                'Duplicate element definition %s = %r in %s'
                % (name, desc, self.layout))
        e = self.desc2elem(name, desc, **kw)
        if e is None:
            return
        self._names[name] = e
        return e

    def create_element(self, desc_name):
        #~ logger.debug("create_element(%r)", desc_name)
        name, pkw = self.splitdesc(desc_name)
        if name in self._names:
            raise Exception(
                'Duplicate element definition %s = %r in %s'
                % (name, desc_name, self.layout))
        desc = getattr(self.layout, name, None)
        if desc is not None:
            return self.define_panel(name, desc, **pkw)
        e = create_layout_element(self, name, **pkw)
        if e is None:
            return None  # e.g. NullField
        if name in self.hidden_elements:
            if isinstance(self.layout, FormLayout):
                return None
            if isinstance(e, list):  # it is a babelfield
                for be in e:
                    be.hidden = True
            else:
                e.hidden = True
        
        self.layout.setup_element(self, e)
        self._names[name] = e
        return e

    def splitdesc(self, picture):
        kw = dict()
        if picture.endswith(')'):
            raise Exception("No longer supported since 20120630")
            a = picture.split("(", 1)
            if len(a) == 2:
                pkw = eval('dict(' + a[1])
                kw.update(pkw)
                picture = a[0]
                #~ return a[0],kw
        a = picture.split(":", 1)
        if len(a) == 1:
            return picture, {}
        if len(a) == 2:
            name = a[0]
            a = a[1].split("x", 1)
            if len(a) == 1:
                kw.update(width=int(a[0]))
                #~ return name, dict(width=int(a[0]))
                return name, kw
            elif len(a) == 2:
                kw.update(width=int(a[0]), height=int(a[1]))
                #~ return name, dict(width=int(a[0]),height=int(a[1]))
                return name, kw
        raise Exception("Invalid picture descriptor %s" % picture)

    def use_as_wildcard(self, de):
        if de.name.endswith('_ptr'):
            return False
        if isinstance(self.layout, ListLayout):
            if de.name == self.layout._datasource.master_key:
                return False
        return True

    def get_data_elem(self, name):
        return self.layout.get_data_elem(name)

    def get_choices_url(self, *args, **kw):
        return self.layout.get_choices_url(
            settings.SITE.kernel.default_renderer.plugin,
            *args, **kw)


class BaseLayout(object):

    _handle_class = LayoutHandle

    _datasource = None

    window_size = None
    """
    A tuple `(width, height)` that specifies the size of the window to be used for this layout.
    For example, specifying `window_size=(50, 30)` means "50 characters wide and 30 lines high".
    The `height` value can also be the string ``'auto'``.
    """

    main = None

    def __init__(self, main=None, datasource=None, hidden_elements=None, **kw):
        """
        datasource is either an actor or an action.
        """
        self._labels = self.override_labels()
        self._added_panels = dict()
        #~ self._window_size = window_size
        self.hidden_elements = hidden_elements or frozenset()
        self._element_options = dict()
        if main is not None:
            self.main = main
        #~ elif not hasattr(self,'main'):
        elif self.main is None:
            raise Exception(
                "Cannot instantiate %s without `main`." % self.__class__)
        self.set_datasource(datasource)
        for k, v in kw.items():
            #~ if not hasattr(self,k):
                #~ raise Exception("Got unexpected keyword %s=%r" % (k,v))
            setattr(self, k, v)

    def set_datasource(self, ds):
        self._datasource = ds
        if ds is not None:
            if isinstance(self.hidden_elements, basestring):
                self.hidden_elements = set(fields_list(
                    ds, self.hidden_elements))
            self.hidden_elements = self.hidden_elements | ds.hidden_elements
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
        Removes specified element names from this Panel's `main` template.
        """
        for name in args:
            self.main = self.main.replace(name, '')

    def setup_handle(self, lh):
        pass

    def setup_element(self, lh, e):
        pass

    def update(self, **kw):
        """
        Update the template of one or more panels.
        """
        #~ if hasattr(self,'_extjs3_handle'):
            #~ raise Exception("Cannot update form layout after UI has been set up.")
        for k, v in kw.items():
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

    #~ @classmethod
    def _add_panel(self, name, tpl, label, options):
        if tpl is None:
            return  # when does this occur?
        if hasattr(self, name):
            raise Exception("Oops: %s has already a name %r" % (self, name))
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

    #~ @classmethod
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

    def get_layout_handle(self, ui):
        """
        Same code as lino.ui.base.Handled.get_handle,
        except that here it's an instance method.
        """
        hname = constants._handle_attr_name

        # we do not want any inherited handle
        h = self.__dict__.get(hname, None)
        if h is None:
            h = self._handle_class(self)
            setattr(self, hname, h)
        return h

    def __str__(self):
        #~ return "%s Detail(%s)" % (self._datasource,[str(x) for x in self.layouts])
        return "%s on %s" % (self.__class__.__name__, self._datasource)

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


class FieldLayout(BaseLayout):
    pass


class FormLayout(FieldLayout):

    join_str = "\n"


class ListLayout(FieldLayout):

    join_str = " "

    def set_datasource(self, ds):
        if ds is None:
            raise Exception("20130327 No datasource for %r" % self)
        super(ListLayout, self).set_datasource(ds)


class ParamsLayout(BaseLayout):

    join_str = " "
    url_param_name = constants.URL_PARAM_PARAM_VALUES
    params_store = None

    def get_data_elem(self, name):
        return self._datasource.get_param_elem(name)

    def setup_handle(self, lh):
        from lino.ui import store
        self.params_store = store.ParameterStore(lh, self.url_param_name)


class ActionParamsLayout(ParamsLayout):
    join_str = "\n"
    window_size = (50, 'auto')
    url_param_name = constants.URL_PARAM_FIELD_VALUES

    def setup_element(self, lh, e):
        from lino.utils import jsgen
        e.declare_type = jsgen.DECLARE_THIS

    def get_choices_url(self, ui, field, **kw):
        return settings.SITE.build_admin_url(
            "apchoices",
            self._datasource.defining_actor.app_label,
            self._datasource.defining_actor.__name__,
            self._datasource.action_name,
            field.name, **kw)


def create_layout_panel(lh, name, vertical, elems, **kw):
    """
    This also must translate ui-agnostic parameters
    like `label_align` to their ExtJS equivalent `labelAlign`.
    """
    from lino.ui import elems as ext_elems
    pkw = dict()
    pkw.update(labelAlign=kw.pop('label_align', 'top'))
    pkw.update(hideCheckBoxLabels=kw.pop('hideCheckBoxLabels', True))
    pkw.update(label=kw.pop('label', None))
    pkw.update(width=kw.pop('width', None))
    pkw.update(height=kw.pop('height', None))
    v = kw.pop('required', NOT_PROVIDED)
    if v is not NOT_PROVIDED:
        pkw.update(required=v)
    if kw:
        raise Exception("Unknown panel attributes %r for %s" % (kw, lh))
    if name == 'main':
        if isinstance(lh.layout, ListLayout):
            e = ext_elems.GridElement(
                lh, name, lh.layout._datasource, *elems, **pkw)
        elif isinstance(lh.layout, ActionParamsLayout):
            e = ext_elems.ActionParamsPanel(lh, name, vertical, *elems, **pkw)
        elif isinstance(lh.layout, ParamsLayout):
            e = ext_elems.ParamsPanel(lh, name, vertical, *elems, **pkw)
        elif isinstance(lh.layout, FormLayout):
            if len(elems) == 1 or vertical:
                e = ext_elems.DetailMainPanel(
                    lh, name, vertical, *elems, **pkw)
            else:
                e = ext_elems.TabPanel(lh, name, *elems, **pkw)
        else:
            raise Exception("No element class for layout %r" % lh.layout)
        return e
    return ext_elems.Panel(lh, name, vertical, *elems, **pkw)


def create_layout_element(lh, name, **kw):
    """
    Create a layout element from the named data element.
    """
    from lino.utils.mldbc.fields import BabelCharField, BabelTextField
    from lino.ui import elems as ext_elems
    from lino.core import fields
    from lino.core import tables
    from lino.utils.jsgen import js_code

    if settings.SITE.catch_layout_exceptions:
        try:
            de = lh.get_data_elem(name)
        except Exception as e:
            # logger.exception(e) removed 20130422 because it caused
            # disturbing output when running tests
            de = None
            name += " (" + str(e) + ")"
    else:
        de = lh.get_data_elem(name)

    if isinstance(de, type) and issubclass(de, fields.Dummy):
        return None

    if isinstance(de, fields.DummyField):
        lh.add_store_field(de)
        return None

    if isinstance(de, fields.Constant):
        return ext_elems.ConstantElement(lh, de, **kw)

    if isinstance(de, SingleRelatedObjectDescriptor):
        return ext_elems.SingleRelatedObjectElement(lh, de.related, **kw)
        #~ return create_field_element(lh,de.related.field,**kw)

    if isinstance(de, fields.RemoteField):
        return create_field_element(lh, de, **kw)
    if isinstance(de, models.Field):
        if isinstance(de, (BabelCharField, BabelTextField)):
            if len(settings.SITE.BABEL_LANGS) > 0:
                elems = [create_field_element(lh, de, **kw)]
                for lang in settings.SITE.BABEL_LANGS:
                    #~ bf = lh.get_data_elem(name+'_'+lang)
                    bf = lh.get_data_elem(name + lang.suffix)
                    elems.append(create_field_element(lh, bf, **kw))
                return elems
        return create_field_element(lh, de, **kw)

    #~ if isinstance(de,fields.LinkedForeignKey):
        # ~ de.primary_key = False # for ext_store.Store()
        #~ lh.add_store_field(de)
        #~ return ext_elems.LinkedForeignKeyElement(lh,de,**kw)

    if isinstance(de, generic.GenericForeignKey):
        # create a horizontal panel with 2 comboboxes
        #~ print 20111123, name,de.ct_field + ' ' + de.fk_field
        #~ return lh.desc2elem(panelclass,name,de.ct_field + ' ' + de.fk_field,**kw)
        #~ return ext_elems.GenericForeignKeyField(lh,name,de,**kw)
        de.primary_key = False  # for ext_store.Store()
        lh.add_store_field(de)
        return ext_elems.GenericForeignKeyElement(lh, de, **kw)

    if isinstance(de, type) and issubclass(de, tables.AbstractTable):
        # The data element refers to a table.
        kw.update(master_panel=js_code("this"))
        if isinstance(lh.layout, FormLayout):
            # When a table is specified in the layout a DetailWindow,
            # then it will be rendered as a panel that displays a
            # "summary" of that table. The panel will have a tool
            # button to "open that table in its own window". The
            # format of that summary is defined by the
            # `slave_grid_format` of the table. `slave_grid_format` is
            # a string with one of the following values:

            kw.update(tools=[
                js_code("Lino.show_in_own_window_button(Lino.%s)" %
                      de.default_action.full_name())])
            if de.slave_grid_format == 'grid':
                kw.update(hide_top_toolbar=True)
                if de.preview_limit is not None:
                    kw.update(preview_limit=de.preview_limit)
                return ext_elems.GridElement(lh, name, de, **kw)

            elif de.slave_grid_format == 'html':
                if de.editable:
                    a = de.insert_action
                    if a is not None:
                        kw.update(ls_insert_handler=js_code("Lino.%s" %
                                  a.full_name()))
                        kw.update(ls_bbar_actions=[
                            settings.SITE.plugins.extjs.renderer.a2btn(a)])
                field = fields.HtmlBox(verbose_name=de.label)
                field.name = de.__name__
                field.help_text = de.help_text
                field._return_type_for_method = de.slave_as_html_meth()
                lh.add_store_field(field)
                e = ext_elems.HtmlBoxElement(lh, field, **kw)
                e.add_requirements(**de.required)
                return e

            elif de.slave_grid_format == 'summary':
                e = ext_elems.SlaveSummaryPanel(lh, de, **kw)
                lh.add_store_field(e.field)
                return e
            else:
                raise Exception(
                    "Invalid slave_grid_format %r" % de.slave_grid_format)

        else:
            raise Exception("No longer supported. Is it being used at all?")
            field = fields.HtmlBox(verbose_name=de.label)
            field.name = de.__name__
            field._return_type_for_method = de.slave_as_summary_meth(', ')
            lh.add_store_field(field)
            e = ext_elems.HtmlBoxElement(lh, field, **kw)
            return e

    if isinstance(de, fields.VirtualField):
        return create_vurt_element(lh, name, de, **kw)

    if callable(de):
        rt = getattr(de, 'return_type', None)
        if rt is not None:
            return create_meth_element(lh, name, de, rt, **kw)

    if not name in ('__str__', '__unicode__', 'name', 'label'):
        value = getattr(lh, name, None)
        if value is not None:
            return value

    # One last possibility is that the app has been hidden. In that
    # case we want the element to simply disappear, similar as if the
    # user had no view permission.

    s = name.split('.')
    if len(s) == 2:
        if settings.SITE.is_hidden_app(s[0]):
            return None

    # Now we tried everything. Build an error message.

    if hasattr(lh, 'rh'):
        msg = "Unknown element '%s' (%r) referred in layout <%s of %s>." % (
            name, de, lh.layout, lh.rh.actor)
        l = [wde.name for wde in lh.rh.actor.wildcard_data_elems()]
        # VirtualTables don't have a model
        model = getattr(lh.rh.actor, 'model', None)
        if getattr(model, '_lino_slaves', None):
            l += [str(rpt) for rpt in model._lino_slaves.values()]
        msg += " Possible names are %s." % ', '.join(l)
    else:
        #~ logger.info("20121023 create_layout_element %r",lh.layout._datasource)
        #~ l = [de.name for de in lh.layout._datasource.wildcard_data_elems()]
        #~ print(20130202, [f.name for f in lh.layout._datasource.model._meta.fields])
        #~ print(20130202, lh.layout._datasource.model._meta.get_all_field_names())
        msg = "Unknown element '%s' (%r) referred in layout <%s>." % (
            name, de, lh.layout)
        # if de is not None:
        #     msg += " Cannot handle %r" % de
    raise KeyError(msg)


def create_vurt_element(lh, name, vf, **kw):
    #~ assert vf.get.func_code.co_argcount == 2, (name, vf.get.func_code.co_varnames)
    e = create_field_element(lh, vf, **kw)
    if not vf.is_enabled(lh):
        e.editable = False
    return e


def create_meth_element(lh, name, meth, rt, **kw):
    #~ if hasattr(rt,'_return_type_for_method'):
        #~ raise Exception(
          #~ "%s.%s : %r has already an attribute '_return_type_for_method'" % (
            #~ lh,name,rt))
    rt.name = name
    rt._return_type_for_method = meth
    if meth.func_code.co_argcount < 2:
        raise Exception("Method %s has %d arguments (must have at least 2)" %
                        (meth, meth.func_code.co_argcount))
        #~ , (name, meth.func_code.co_varnames)
    #~ kw.update(editable=False)
    e = create_field_element(lh, rt, **kw)
    #~ if lh.rh.actor.actor_id == 'contacts.Persons':
        #~ print 'ext_ui.py create_meth_element',name,'-->',e
    #~ if name == 'preview':
        #~ print 20110714, 'ext_ui.create_meth_element', meth, repr(e)
    return e
    #~ e = lh.main_class.field2elem(lh,return_type,**kw)
    #~ assert e.field is not None,"e.field is None for %s.%s" % (lh.layout,name)
    #~ lh._store_fields.append(e.field)
    #~ return e

    #~ if rt is None:
        #~ rt = models.TextField()

    #~ e = ext_elems.MethodElement(lh,name,meth,rt,**kw)
    #~ assert e.field is not None,"e.field is None for %s.%s" % (lh.layout,name)
    #~ lh._store_fields.append(e.field)
    #~ return e


def create_field_element(lh, field, **kw):
    #~ e = lh.main_class.field2elem(lh,field,**kw)
    from lino.ui import elems as ext_elems
    e = ext_elems.field2elem(lh, field, **kw)
    assert e.field is not None, "e.field is None for %s.%s" % (lh.layout, kw)
    lh.add_store_field(e.field)
    return e
    # return FieldElement(field,**kw)
