# Copyright 2012-2013 Luc Saffre
# License: BSD (see file COPYING for details)

"""
The :xfile:`models.py` for the :mod:`lino.modlib.about` app.

"""

import logging
logger = logging.getLogger(__name__)

import os
import cgi
import inspect
import types
import datetime

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings


from lino.utils import AttrDict
from lino.utils.xmlgen import html as xghtml

from lino.utils.code import codetime, codefiles, SourceFile
from lino import mixins
from lino import dd, rt


from lino.utils.xmlgen import html as xghtml
E = xghtml.E


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
    required = dict(user_level='admin')
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


class About(mixins.EmptyTable):

    """
    A modal window displaying information about this server.
    """
    label = _("About")
    help_text = _("Show information about this site.")
    required = dict(auth=False)
    #~ hide_window_title = True
    hide_top_toolbar = True
    #~ window_size = (700,400)
    #~ detail_layout = AboutDetail(window_size = (700,400))
    #~ detail_layout = AboutDetail()
    detail_layout = dd.FormLayout("""
    about_html
    server_status
    """, window_size=(60, 20))

    #~ versions = dd.Constant(lino.welcome_html())

    #~ do_build = BuildSiteCache()

    #~ @classmethod
    #~ def setup_actions(self):
        #~ super(About,self).setup_actions()
        #~ self.add_action(BuildSiteCache())

    #~ @dd.constant(_("Versions"))
    #~ @dd.constant()
    #~ def versions(cls,ui):
        #~ return settings.SITE.welcome_html(ui)

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
                    len(settings.SITE.ui.pending_threads)))
        return E.div(*body, class_='htmlText')

    #~ @dd.displayfield(_("Versions"))
    #~ def versions(self,obj,ar):
        #~ return lino.welcome_html(ar.ui)

    #~ @dd.constantfield(_("Versions"))
    #~ def versions(cls,self,req):
        #~ return lino.welcome_html()

    #~ @dd.virtualfield(models.DateTimeField(_("Server up since")))
    #~ def startup_time(cls,self,req):
        #~ return settings.SITE.startup_time


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


#~ def _test():
    #~ import doctest
    #~ doctest.testmod()
#~ if __name__ == "__main__":
    #~ _test()
def setup_site_menu(site, ui, profile, m):
    m.add_action(site.modules.about.About)
    if settings.SITE.use_experimental_features:
        m.add_action(site.modules.about.Models)
        m.add_action(site.modules.about.Inspector)
        m.add_action(site.modules.about.SourceFiles)
