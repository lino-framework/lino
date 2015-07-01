# Copyright 2012-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Database models for `lino.modlib.about`.

"""

import logging
logger = logging.getLogger(__name__)

import os
import cgi
import inspect
import types
import datetime

from textwrap import fill

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings


from lino.modlib.extjs.elems import Panel
from lino.utils.report import EmptyTable
from lino.utils import AttrDict

from lino.utils.code import codetime, codefiles, SourceFile
from lino.utils.xmlgen.html import E
from lino.utils.diag import get_window_actions, have_action

from lino.api import dd


class Models(dd.VirtualTable):
    label = _("Models")
    #~ column_defaults = dict(width=8)
    #~ column_names = "app name verbose_name docstring rows"
    column_names = "app name docstring rows detail_action"
    detail_layout = """
    app name docstring rows
    about.FieldsByModel
    """

    slave_grid_format = 'html'

    @classmethod
    def get_data_rows(self, ar):
        #~ profile = ar.get_user().profile
        for model in models.get_models():
            if True:
                #~ print model
                yield model

    @classmethod
    def summary_row(cls, ar, obj, **kw):
        return [unicode(obj._meta.verbose_name_plural)]

    @dd.displayfield(_("app_label"))
    def app(self, obj, ar):
        return obj._meta.app_label

    @dd.displayfield(_("name"))
    def name(self, obj, ar):
        return obj.__name__

    #~ @dd.displayfield(_("Detail Action"))
    @dd.displayfield()
    def detail_action(self, obj, ar):
        if obj.get_default_table().detail_action is None:
            return ''
        return obj.get_default_table().detail_action.full_name()

    #~ @dd.displayfield(_("verbose name"))
    #~ def vebose_name(self,obj,ar):
        #~ return unicode(obj._meta.vebose_name)

    @dd.displayfield(_("docstring"))
    def docstring(self, obj, ar):
        return obj.__doc__
        #~ return restify(unicode(obj.__doc__))

    @dd.requestfield(_("Rows"))
    def rows(self, obj, ar):
        return obj.get_default_table().request(
            ar.ui,
            user=ar.get_user(), renderer=ar.renderer)


class FieldsByModel(dd.VirtualTable):
    label = _("Fields")
    #~ master_key = "model"
    #~ master = Models
    column_names = "name verbose_name help_text_column"

    @classmethod
    def get_data_rows(self, ar):
        model = ar.master_instance
        if model:
            for (fld, remote) in model._meta.get_fields_with_model():
                yield fld

    @dd.displayfield(_("name"))
    def name(self, fld, ar):
        return fld.name

    @dd.displayfield(_("verbose name"))
    def verbose_name(self, fld, ar):
        return unicode(fld.vebose_name)

    @dd.displayfield(_("help text"))
    def help_text_column(self, obj, ar):
        #~ return obj.__doc__
        return restify(unicode(obj.help_text))


class Inspected(object):

    def __init__(self, parent, prefix, name, value):
        self.parent = parent
        self.prefix = prefix
        self.name = name
        self.value = value


class Inspector(dd.VirtualTable):
    """
    Shows a simplistic "inspector" which once helped me for debugging.
    Needs more work to become seriously useful...
    
    """
    label = _("Inspector")
    required_roles = dd.required(dd.SiteStaff)
    column_names = "i_name i_type i_value"
    parameters = dict(
        inspected=models.CharField(
            _("Inspected object"), max_length=100, blank=True),
        show_callables=models.BooleanField(_("show callables"), default=False)
    )
    params_layout = 'inspected show_callables'
    #~ editable = False
    #~ slave_grid_format = 'html'

    @classmethod
    def get_inspected(self, name):
        #~ ctx = dict(settings=settings,lino=lino)
        if not name:
            return settings
        try:
            o = eval('settings.' + name)
        except Exception, e:
            o = e
        return o

        #~ o = settings
        #~ try:
            #~ for ch in name.split('.'):
                #~ o = getattr(o,ch)
        #~ except Exception,e:
            #~ o = e
        #~ return o

    @classmethod
    def get_data_rows(self, ar):
        #~ logger.info("20120210 %s, %s",ar.quick_search,ar.param_values.inspected)

        if ar.param_values.show_callables:
            def flt(v):
                return True
        else:
            def flt(v):
                if isinstance(v, (
                    types.FunctionType,
                    types.GeneratorType,
                    types.UnboundMethodType,
                    types.UnboundMethodType,
                    types.BuiltinMethodType,
                    types.BuiltinFunctionType,
                )):
                    return False
                return True

        o = self.get_inspected(ar.param_values.inspected)
        if isinstance(o, (list, tuple)):
            for i, v in enumerate(o):
                k = "[" + str(i) + "]"
                yield Inspected(o, '', k, v)
        elif isinstance(o, AttrDict):
            for k, v in o.items():
                yield Inspected(o, '.', k, v)
        elif isinstance(o, dict):
            for k, v in o.items():
                k = "[" + repr(k) + "]"
                yield Inspected(o, '', k, v)
        else:
            for k in dir(o):
                if not k.startswith('__'):
                    if not ar.quick_search or (ar.quick_search.lower() in k.lower()):
                        v = getattr(o, k)
                        if flt(v):
                        #~ if not inspect.isbuiltin(v) and not inspect.ismethod(v):
                            #~ if ar.param_values.show_callables or not inspect.isfunction(v):
                            #~ if isinstance(v,types.FunctionType ar.param_values.show_callables or not callable(v):
                            yield Inspected(o, '.', k, v)
        #~ for k,v in o.__dict__.items():
            #~ yield Inspected(o,k,v)

    @dd.displayfield(_("Name"))
    def i_name(self, obj, ar):
        pv = dict()
        if ar.param_values.inspected:
            pv.update(inspected=ar.param_values.inspected +
                      obj.prefix + obj.name)
        else:
            pv.update(inspected=obj.name)
        #~ newreq = ar.spawn(ar.ui,user=ar.user,renderer=ar.renderer,param_values=pv)
        newreq = ar.spawn(param_values=pv)
        return ar.href_to_request(newreq, obj.name)
        #~ return obj.name

    @dd.displayfield(_("Value"))
    def i_value(self, obj, ar):
        return cgi.escape(unicode(obj.value))

    @dd.displayfield(_("Type"))
    def i_type(self, obj, ar):
        return cgi.escape(str(type(obj.value)))


#~ class AboutDetail(dd.FormLayout):
    #~ """
    #~ The Detail Layout for :class:`About`
    #~ """
    #~ window_size = (60,30)
    #~ main = """
    #~ versions:40x5 startup_time:30
    #~ about.Models:70x10
    #~ """

if False:

  class DetailLayouts(dd.VirtualTable):
    """Shows a list of all detail layouts
    (:attr:`lino.core.actors.Actor.detail_layout`) defined in this
    application.

    """
    column_names = "datasource viewable_for fields"

    @classmethod
    def get_data_rows(self, ar):
        from lino.core.actors import actors_list
        coll = set()
        for a in actors_list:
            if a.detail_layout:
                coll.add(a.detail_layout)

        l = list(coll)

        def f(a, b):
            return cmp(str(a._datasource), str(b._datasource))
        return sorted(l, f)

    @dd.displayfield(_("Datasource"))
    def datasource(self, obj, ar):
        return str(obj._datasource)

    @dd.displayfield(_("Viewable for"))
    def viewable_for(self, obj, ar):
        return have_action(obj._datasource.detail_action)

    @dd.displayfield(_("Fields"))
    def fields(self, obj, ar):
        lh = obj.get_layout_handle(settings.SITE.kernel.default_ui)
        # elems = [e.name for e in lh._names.values() if not e.hidden]
        elems = [f.name for f in lh._store_fields]
        return fill(' '.join(elems), 60)


  class WindowActions(dd.VirtualTable):
    """Shows a list of all window actions defined in this application.

    """
    column_names = "full_name viewable_for fields"

    @classmethod
    def get_data_rows(self, ar):
        l = list(get_window_actions().values())

        def f(a, b):
            return cmp(a.full_name(), b.full_name())
        return sorted(l, f)

    @dd.displayfield(_("Name"))
    def full_name(self, obj, ar):
        return obj.full_name()

    @dd.displayfield(_("Viewable for"))
    def viewable_for(self, obj, ar):
        return have_action(obj)

    @dd.displayfield(_("Fields"))
    def fields(self, obj, ar):
        wl = obj.get_window_layout() or obj.action.params_layout
        if wl is None:
            return ''
        lh = wl.get_layout_handle(settings.SITE.kernel.default_ui)
        elems = [str(f.name) for f in lh._store_fields]
        #return ' '.join([repr(type(e)) for e in elems])
        # print 20150210, elems
        # return str(len(elems))
        # return ' '.join(elems)
        return fill(' '.join(elems), 50)


  class FormPanels(dd.VirtualTable):
    """Shows a list of all form panels defined in this application.

    """
    column_names = "full_name viewable_for fields"

    @classmethod
    def get_data_rows(self, ar):
        coll = set()
        for ba in get_window_actions().values():
            wl = ba.get_window_layout() or ba.action.params_layout
            if wl is not None:
                lh = wl.get_layout_handle(settings.SITE.kernel.default_ui)
                for e in lh.main.walk():
                    if e.__class__ is Panel:
                        if e.label is not None:
                            coll.add(e)

        def f(a, b):
            return cmp(
                str(a.layout_handle.layout._datasource),
                str(b.layout_handle.layout._datasource))
        return sorted(list(coll), f)

    @dd.displayfield(_("Name"))
    def full_name(self, obj, ar):
        return "{0}.{1}\n{2}".format(
            obj.layout_handle.layout._datasource, obj.name,
            unicode(obj.label))

    @dd.displayfield(_("Viewable for"))
    def viewable_for(self, obj, ar):
        return have_action(obj)

    @dd.displayfield(_("Fields"))
    def fields(self, obj, ar):
        elems = [e.name for e in obj.walk()]
        return fill(' '.join(elems), 40)


class About(EmptyTable):
    """Display information about this web site.  This defines the window
    which opens via the menu command :menuselection:`Site --> About`.

    """
    label = _("About")
    help_text = _("Show information about this site.")
    required_roles = set()
    hide_top_toolbar = True
    detail_layout = dd.FormLayout("""
    about_html
    server_status
    """, window_size=(60, 20))

    @dd.constant()
    def about_html(cls):

        body = []

        body.append(settings.SITE.welcome_html())

        #~ print "20121112 startup_time", settings.SITE.startup_time.date()
        def dtfmt(dt):
            if isinstance(dt, float):
                dt = datetime.datetime.fromtimestamp(dt)
                #~ raise ValueError("Expected float, go %r" % dt)
            return unicode(_("%(date)s at %(time)s")) % dict(
                date=dd.fdf(dt.date()),
                time=dt.time())

        items = []
        times = []
        value = settings.SITE.startup_time
        label = _("Server uptime")
        body.append(E.p(unicode(label), ' : ', E.b(dtfmt(value))))
        body.append(E.p(unicode(_("Source timestamps:"))))
        for src in ("lino", "lino_welfare", 'django', 'atelier'):
            label = src
            value = codetime('%s.*' % src)
            if value is not None:
                times.append((label, value))

        def mycmp(a, b):
            return cmp(b[1], a[1])
        times.sort(mycmp)
        for label, value in times:
            items.append(E.li(unicode(label), ' : ', E.b(dtfmt(value))))
        body.append(E.ul(*items))
        return E.div(*body, class_='htmlText')

    @dd.displayfield(_("Server status"))
    def server_status(cls, obj, ar):
        body = []
        body.append(E.p(_("%s pending threads") %
                    len(settings.SITE.kernel.pending_threads)))
        return E.div(*body, class_='htmlText')


class SourceFiles(dd.VirtualTable):
    label = _("Source files")
    column_names = 'module_name code_lines doc_lines'

    @classmethod
    def get_data_rows(self, ar):
        for name, filename in codefiles('lino*'):
            yield SourceFile(name, filename)

    @dd.virtualfield(models.IntegerField(_("Code")))
    def code_lines(self, obj, ar):
        return obj.count_code

    @dd.virtualfield(models.IntegerField(_("doc")))
    def doc_lines(self, obj, ar):
        return obj.count_doc

    @dd.virtualfield(models.CharField(_("module name")))
    def module_name(self, obj, ar):
        return obj.modulename

