# Copyright 2012-2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Database models for `lino.modlib.about`.

"""
from past.builtins import cmp
from builtins import str
from builtins import object

import logging
logger = logging.getLogger(__name__)

import cgi
import types
import datetime

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings


from lino.utils.report import EmptyTable
from lino.utils import AttrDict

from lino.utils.code import codetime, codefiles, SourceFile
from lino.utils.xmlgen.html import E

from lino.api import dd


class Models(dd.VirtualTable):
    label = _("Models")
    # column_defaults = dict(width=8)
    # column_names = "app name verbose_name docstring rows"
    column_names = "app name docstring rows detail_action"
    detail_layout = """
    app name docstring rows
    about.FieldsByModel
    """

    slave_grid_format = 'html'

    @classmethod
    def get_data_rows(self, ar):
        # profile = ar.get_user().profile
        for model in models.get_models():
            if True:
                # print model
                yield model

    @classmethod
    def summary_row(cls, ar, obj, **kw):
        return [str(obj._meta.verbose_name_plural)]

    @dd.displayfield(_("app_label"))
    def app(self, obj, ar):
        return obj._meta.app_label

    @dd.displayfield(_("name"))
    def name(self, obj, ar):
        return obj.__name__

    # @dd.displayfield(_("Detail Action"))
    @dd.displayfield()
    def detail_action(self, obj, ar):
        if obj.get_default_table().detail_action is None:
            return ''
        return obj.get_default_table().detail_action.full_name()

    # @dd.displayfield(_("verbose name"))
    # def vebose_name(self,obj,ar):
        # return unicode(obj._meta.vebose_name)

    @dd.displayfield(_("docstring"))
    def docstring(self, obj, ar):
        return obj.__doc__
        # return restify(unicode(obj.__doc__))

    @dd.requestfield(_("Rows"))
    def rows(self, obj, ar):
        return obj.get_default_table().request(
            ar.ui,
            user=ar.get_user(), renderer=ar.renderer)


class FieldsByModel(dd.VirtualTable):
    label = _("Fields")
    # master_key = "model"
    # master = Models
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
        return str(fld.vebose_name)

    @dd.displayfield(_("help text"))
    def help_text_column(self, obj, ar):
        # return obj.__doc__
        return restify(str(obj.help_text))


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
    # editable = False
    # slave_grid_format = 'html'

    @classmethod
    def get_inspected(self, name):
        # ctx = dict(settings=settings,lino=lino)
        if not name:
            return settings
        try:
            o = eval('settings.' + name)
        except Exception as e:
            o = e
        return o


    @classmethod
    def get_data_rows(self, ar):
        # logger.info("20120210 %s, %s",ar.quick_search,ar.param_values.inspected)

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
                    types.BuiltinFunctionType
                )):
                    return False
                return True

        o = self.get_inspected(ar.param_values.inspected)
        if isinstance(o, (list, tuple)):
            for i, v in enumerate(o):
                k = "[" + str(i) + "]"
                yield Inspected(o, '', k, v)
        elif isinstance(o, AttrDict):
            for k, v in list(o.items()):
                yield Inspected(o, '.', k, v)
        elif isinstance(o, dict):
            for k, v in list(o.items()):
                k = "[" + repr(k) + "]"
                yield Inspected(o, '', k, v)
        else:
            for k in dir(o):
                if not k.startswith('__'):
                    if not ar.quick_search or (
                            ar.quick_search.lower() in k.lower()):
                        v = getattr(o, k)
                        if flt(v):
                        # if not inspect.isbuiltin(v) and not inspect.ismethod(v):
                        #     if ar.param_values.show_callables or not inspect.isfunction(v):
                        #     if isinstance(v,types.FunctionType ar.param_values.show_callables or not callable(v):
                            yield Inspected(o, '.', k, v)
        # for k,v in o.__dict__.items():
            # yield Inspected(o,k,v)

    @dd.displayfield(_("Name"))
    def i_name(self, obj, ar):
        pv = dict()
        if ar.param_values.inspected:
            pv.update(inspected=ar.param_values.inspected +
                      obj.prefix + obj.name)
        else:
            pv.update(inspected=obj.name)
        # newreq = ar.spawn(ar.ui,user=ar.user,renderer=ar.renderer,param_values=pv)
        newreq = ar.spawn(param_values=pv)
        return ar.href_to_request(newreq, obj.name)
        # return obj.name

    @dd.displayfield(_("Value"))
    def i_value(self, obj, ar):
        return cgi.escape(str(obj.value))

    @dd.displayfield(_("Type"))
    def i_type(self, obj, ar):
        return cgi.escape(str(type(obj.value)))


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

        if settings.SITE.languages:
            body.append(E.p(str(_("Languages")) + ": " + ', '.join([
                lng.django_code for lng in settings.SITE.languages])))

        # print "20121112 startup_time", settings.SITE.startup_time.date()
        def dtfmt(dt):
            if isinstance(dt, float):
                dt = datetime.datetime.fromtimestamp(dt)
                # raise ValueError("Expected float, go %r" % dt)
            return str(_("%(date)s at %(time)s")) % dict(
                date=dd.fdf(dt.date()),
                time=dt.time())

        items = []
        times = []
        value = settings.SITE.startup_time
        label = _("Server uptime")
        body.append(E.p(str(label), ' : ', E.b(dtfmt(value))))
        if settings.SITE.is_demo_site:
            s = str(_("This is a Lino demo site."))
            body.append(E.p(s))
        if settings.SITE.the_demo_date:
            s = _("We are running with simulated date set to {0}.").format(
                dd.fdf(settings.SITE.the_demo_date))
            body.append(E.p(s))
        body.append(E.p(str(_("Source timestamps:"))))
        for src in ("lino", "lino_welfare", 'django', 'atelier'):
            label = src
            value = codetime('%s.*' % src)
            if value is not None:
                times.append((label, value))

        def mycmp(a, b):
            return cmp(b[1], a[1])
        times.sort(mycmp)
        for label, value in times:
            items.append(E.li(str(label), ' : ', E.b(dtfmt(value))))
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

