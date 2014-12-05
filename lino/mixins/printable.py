# -*- coding: UTF-8 -*-
# Copyright 2009-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
See :doc:`/admin/printable`

"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

import shutil
import os
from os.path import join, dirname
import logging
import cStringIO
import datetime

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils import translation

from django.template.loader import (select_template, Context,
                                    TemplateDoesNotExist)
from lino import rt
from lino.utils.xmlgen.html import E

davlink = settings.SITE.plugins.get('davlink', None)
has_davlink = davlink is not None and settings.SITE.use_java


from lino.core import actions
from lino.core import dbutils
from lino.utils.choosers import chooser
from lino.utils.appy_pod import Renderer
from lino.core.model import Model
from lino.core.choicelists import Choice, ChoiceList
from lino.mixins.duplicable import Duplicable

from lino.utils.media import MediaFile
from lino.utils.media import TmpMediaFile
from lino.utils.pdf import merge_pdfs


try:
    import ho.pisa as pisa
    # pisa.showLogging()
except ImportError:
    pisa = None

try:
    import pyratemp
except ImportError:
    pyratemp = None


class BuildMethod(Choice):

    """Base class for all build methods.  A build method encapsulates the
    process of generating a "printable document" that inserts data
    from the database into a template, using a given combination of a
    template parser and post-processor.

    """
    target_ext = None
    template_ext = None
    templates_name = None
    cache_name = 'cache'
    default_template = ''

    use_webdav = False
    """Whether this build method results is an editable file.  For
    example, `.odt` files are considered editable while `.pdf` files
    aren't.
    
    In that case the target will be in a webdav folder and the print
    action will respond `open_davlink_url` instead of the usual
    `open_url`, which extjs3 ui will implement by calling
    `Lino.davlink_open()` instead of the usual `window.open()`.
    
    When :mod:`lino.modlib.davlink` is not installed, this setting
    still influences the target path of resulting files, but the
    clients will not automatically recognize them as webdav-editable
    URLs.

    """

    def __init__(self, *args, **kwargs):
        super(BuildMethod, self).__init__(*args, **kwargs)
        if self.templates_name is None:
            self.templates_name = self.name

    def get_target(self, action, elem):
        "used by `get_target_name`"
        return MediaFile(
            self.use_webdav,
            self.cache_name,
            self.name,
            elem.filename_root() + self.target_ext)

    def get_target_name(self, action, elem):
        return self.get_target(action, elem).name

    def get_target_url(self, action, elem):
        return self.get_target(action, elem).url

    def build(self, ar, action, elem):
        raise NotImplementedError


class DjangoBuildMethod(BuildMethod):

    """
    Using Django's templating engine.
    """

    def get_template(self, action, elem):
        tpls = action.get_print_templates(self, elem)
        if len(tpls) == 0:
            raise Warning("No templates defined for %r" % elem)
        #~ logger.debug('make_pisa_html %s',tpls)
        try:
            return select_template(tpls)
        except TemplateDoesNotExist, e:
            raise Warning("No template found for %s (%s)" % (e, tpls))

    # ,MEDIA_URL=settings.MEDIA_URL):
    def render_template(self, elem, tpl, **context):
        context.update(
            instance=elem,
            title=unicode(elem),
            MEDIA_URL=settings.MEDIA_ROOT.replace('\\', '/') + '/',
        )
        return tpl.render(Context(context))


class PisaBuildMethod(DjangoBuildMethod):

    """
    Generates .pdf files from .html templates.
    Usage example see :ref:`lino.tutorials.pisa`.
    """
    # name = 'pisa'
    target_ext = '.pdf'
    template_ext = '.pisa.html'

    def build(self, ar, action, elem):
        tpl = self.get_template(action, elem)
        filename = action.before_build(self, elem)
        if filename is None:
            return
        #~ html = self.render_template(elem,tpl,request=ar.request)
        html = self.render_template(elem, tpl, ar=ar)
        html = html.encode("utf-8")
        file(filename + '.html', 'w').write(html)

        result = cStringIO.StringIO()
        h = logging.FileHandler(filename + '.log', 'w')
        pisa.log.addHandler(h)
        pdf = pisa.pisaDocument(
            cStringIO.StringIO(html), result, encoding='utf-8')
        pisa.log.removeHandler(h)
        h.close()
        fd = file(filename, 'wb')
        fd.write(result.getvalue())
        fd.close()
        if pdf.err:
            raise Exception("pisa.pisaDocument.err is %r" % pdf.err)
        return os.path.getmtime(filename)


class SimpleBuildMethod(BuildMethod):

    def get_template_leaf(self, action, elem):

        tpls = action.get_print_templates(self, elem)
        if len(tpls) != 1:
            raise Exception(
                "%s.get_print_templates() must return "
                "exactly 1 template (got %r)" % (
                    elem.__class__.__name__, tpls))
        tpl_leaf = tpls[0]
        lang = elem.get_print_language()
        if lang != settings.SITE.DEFAULT_LANGUAGE.django_code:
            name = tpl_leaf[:-len(self.template_ext)] + \
                "_" + lang + self.template_ext
            if rt.find_config_file(
                    name, *elem.get_template_groups()):
                return name
        return tpl_leaf

    def get_template_file(self, ar, action, elem):
        tpl_leaf = self.get_template_leaf(action, elem)
        groups = elem.get_template_groups()
        tplfile = settings.SITE.find_config_file(tpl_leaf, *groups)
        if not tplfile:
            raise Warning("No file %s in %s" % (tpl_leaf, groups))
        return tplfile

    def build(self, ar, action, elem):
        #~ if elem is None:
            #~ return
        target = action.before_build(self, elem)
        if not target:
            return
        tplfile = self.get_template_file(ar, action, elem)
        return self.simple_build(ar, elem, tplfile, target)

    def simple_build(self, ar, elem, tpl, target):
        raise NotImplementedError


class AppyBuildMethod(SimpleBuildMethod):

    """
    Base class for Build Methods that use `.odt` templates designed
    for :term:`appy.pod`.
    
    http://appyframework.org/podRenderingTemplates.html
    """

    template_ext = '.odt'
    templates_name = 'appy'  # subclasses use the same templates directory
    default_template = 'Default.odt'

    def simple_build(self, ar, elem, tpl, target):
        #~ from lino.models import get_site_config
        #~ from appy.pod.renderer import Renderer
        #~ renderer = None
        """
        When the source string contains non-ascii characters, then
        we must convert it to a unicode string.
        """
        lang = str(elem.get_print_language())
        logger.info(u"appy.pod render %s -> %s (language=%r,params=%s",
                    tpl, target, lang, settings.SITE.appy_params)

        with translation.override(lang):

            context = elem.get_printable_context(ar=ar)

            # backwards compat for existing .odt templates.  Cannot
            # set this earlier because that would cause "render() got
            # multiple values for keyword argument 'self'" exception
            context.update(self=context['this'])

            Renderer(ar, tpl, context, target,
                     **settings.SITE.appy_params).run()
        return os.path.getmtime(target)


class AppyOdtBuildMethod(AppyBuildMethod):

    """
    Generates .odt files from .odt templates.
    
    This method doesn't require OpenOffice nor the
    Python UNO bridge installed
    (except in some cases like updating fields).
    """
    target_ext = '.odt'
    cache_name = 'userdocs'
    #~ cache_name = 'webdav'
    use_webdav = True


class AppyPdfBuildMethod(AppyBuildMethod):
    """
    Generates .pdf files from .odt templates.
    """
    target_ext = '.pdf'


class AppyRtfBuildMethod(AppyBuildMethod):

    """
    Generates .rtf files from .odt templates.
    """
    target_ext = '.rtf'
    cache_name = 'userdocs'
    use_webdav = True


class AppyDocBuildMethod(AppyBuildMethod):

    """
    Generates .doc files from .odt templates.
    """
    target_ext = '.doc'
    cache_name = 'userdocs'
    use_webdav = True


class LatexBuildMethod(BuildMethod):

    """
    Generates .pdf files from .tex templates.
    """
    target_ext = '.pdf'
    template_ext = '.tex'

    def simple_build(self, ar, elem, tpl, target):
        context = dict(instance=elem)
        raise NotImplementedError


class RtfBuildMethod(SimpleBuildMethod):

    """
    Generates .rtf files from .rtf templates.
    """

    target_ext = '.rtf'
    template_ext = '.rtf'
    cache_name = 'userdocs'

    def simple_build(self, ar, elem, tpl, target):
        context = dict(instance=elem)
        t = pyratemp.Template(filename=tpl)
        try:
            result = t(**context)
        except pyratemp.TemplateRenderError, e:
            raise Exception(u"%s in %s" % (e, tpl))
        fd = file(target, 'wb')
        fd.write(result)
        fd.close()
        return os.path.getmtime(target)


class BuildMethods(ChoiceList):
    verbose_name = _("Build method")
    item_class = BuildMethod
    app_label = 'lino'

    @classmethod
    def get_system_default(cls):
        sc = settings.SITE.site_config
        if sc.default_build_method is not None:
            return sc.default_build_method
        if settings.SITE.default_build_method:
            return cls.get_by_value(
                settings.SITE.default_build_method)
        return cls.appyodt  # hard-coded default


def register_build_method(bm):
    BuildMethods.add_item_instance(bm)


register_build_method(AppyOdtBuildMethod('appyodt'))
register_build_method(AppyDocBuildMethod('appydoc'))
register_build_method(AppyPdfBuildMethod('appypdf'))
register_build_method(AppyRtfBuildMethod('appyrtf'))
register_build_method(LatexBuildMethod('latex'))
register_build_method(PisaBuildMethod('pisa'))
register_build_method(RtfBuildMethod('rtf'))


def build_method_choices():
    return BuildMethods.choices


class BasePrintAction(actions.Action):

    """
    Base class for all "Print" actions.
    """
    sort_index = 50
    url_action_name = 'print'
    label = _('Print')

    def attach_to_actor(self, actor, name):
        if not dbutils.resolve_app('system'):
            return False
        # if actor.__name__ == 'ExcerptsByProject':
        #     logger.info("20140401 attach_to_actor() %r", self)
        return super(BasePrintAction, self).attach_to_actor(actor, name)

    def is_callable_from(self, caller):
        return isinstance(caller, (
            actions.GridEdit,
            actions.ShowDetailAction,
            actions.ShowEmptyTable))  # but not from InsertRow

    def get_print_templates(self, bm, elem):
        return elem.get_print_templates(bm, self)

    def before_build(self, bm, elem):
        """Return the target filename if a document needs to be built,
        otherwise return ``None``.
        """
        elem.before_printable_build(bm)
        filename = bm.get_target_name(self, elem)
        if not filename:
            return
        if os.path.exists(filename):
            logger.debug(u"%s %s -> overwrite existing %s.",
                         bm, elem, filename)
            os.remove(filename)
        else:
            #~ logger.info("20121221 makedirs_if_missing %s",os.path.dirname(filename))
            rt.makedirs_if_missing(os.path.dirname(filename))
        logger.debug(u"%s : %s -> %s", bm, elem, filename)
        return filename

    def notify_done(self, ar, bm, leaf, url, **kw):
        help_url = ar.get_help_url("print", target='_blank')
        msg = _("Your printable document (filename %(doc)s) "
                "should now open in a new browser window. "
                "If it doesn't, please consult %(help)s "
                "or ask your system administrator.")
        msg %= dict(doc=leaf, help=E.tostring(help_url))
        kw.update(message=msg, alert=True)
        if bm.use_webdav and has_davlink and ar.request is not None:
            kw.update(
                open_davlink_url=ar.request.build_absolute_uri(url))
        else:
            kw.update(open_url=url)
        ar.success(**kw)
        return


class DirectPrintAction(BasePrintAction):
    """Print using a hard-coded template and no cache.

    """
    url_action_name = None
    icon_name = 'printer'

    def __init__(self, label=None, tplname=None, build_method=None, **kw):
        super(DirectPrintAction, self).__init__(label, **kw)
        self.build_method = build_method
        self.tplname = tplname

    def get_print_templates(self, bm, elem):
        #~ assert bm is self.bm
        if self.tplname:
            return [self.tplname + bm.template_ext]
        return elem.get_print_templates(bm, self)

    def run_from_ui(self, ar, **kw):
        elem = ar.selected_rows[0]
        bm = elem.get_build_method()
        bm.build(ar, self, elem)
        mf = bm.get_target(self, elem)
        # if ar.request is not None and bm.use_webdav and has_davlink:
        #     url = ar.request.build_absolute_uri(url)
        #     kw.update(open_davlink_url=url)
        # else:
        #     kw.update(open_url=url)
        # ar.success(**kw)
        leaf = mf.parts[-1]
        self.notify_done(ar, bm, leaf, mf.url, **kw)


class CachedPrintAction(BasePrintAction):

    """Note that this action should rather be called 'Open a printable
    document' than 'Print'.  For the user they are synonyms as long as
    Lino doesn't support server-side printing.

    """

    # select_rows = False
    http_method = 'POST'
    icon_name = 'printer'

    def before_build(self, bm, elem):
        if elem.build_time:
            return
        return BasePrintAction.before_build(self, bm, elem)

    def run_from_ui(self, ar, **kw):

        if len(ar.selected_rows) == 1:
            obj = ar.selected_rows[0]
            bm = obj.get_build_method()
            mf = bm.get_target(self, obj)

            leaf = mf.parts[-1]
            if obj.build_time is None:
                obj.build_target(ar)
                ar.info("%s has been built.", leaf)
            else:
                ar.info("Reused %s from cache.", leaf)

            self.notify_done(ar, bm, leaf, mf.url, **kw)
            ar.set_response(refresh=True)
            return

        def ok(ar2):
            #~ qs = [ar.actor.get_row_by_pk(pk) for pk in ar.selected_pks]
            mf = self.print_multiple(ar, ar.selected_rows)
            ar2.success(open_url=mf.url)
            #~ kw.update(refresh_all=True)
            #~ return kw
        msg = _("This will print %d rows.") % len(ar.selected_rows)
        ar.confirm(ok, msg, _("Are you sure?"))

    def print_multiple(self, ar, qs):
        pdfs = []
        for obj in qs:
            #~ assert isinstance(obj,CachedPrintable)
            if obj.printed_by_id is None:
                obj.build_target(ar)
            pdf = obj.get_target_name()
            assert pdf is not None
            pdfs.append(pdf)

        mf = TmpMediaFile(ar, 'pdf')
        rt.makedirs_if_missing(os.path.dirname(mf.name))
        merge_pdfs(pdfs, mf.name)
        return mf


class EditTemplate(BasePrintAction):
    """

    """
    sort_index = 51
    url_action_name = 'edit_tpl'
    label = _('Edit Print Template')
    required = dict(user_level='manager')

    def run_from_ui(self, ar, **kw):

        lcd = settings.SITE.confdirs.LOCAL_CONFIG_DIR
        if lcd is None:
            # ar.info("No local config directory in %s " %
            #         settings.SITE.confdirs)
            raise Warning("No local config directory. "
                          "Contact your system administrator.")

        elem = ar.selected_rows[0]
        bm = elem.get_build_method()
        leaf = bm.get_template_leaf(self, elem)

        filename = bm.get_template_file(ar, self, elem)
        local_file = None
        groups = elem.get_template_groups()
        assert len(groups) > 0
        for grp in groups:
            parts = [grp, leaf]
            local_file = join(lcd.name, *parts)
            if filename == local_file:
                break

        parts = ['webdav', 'config'] + parts
        url = settings.SITE.build_media_url(*parts)
        if ar.request is not None:
            url = ar.request.build_absolute_uri(url)

        if not has_davlink:
            msg = "cp %s %s" % (filename, local_file)
            ar.info(msg)
            raise Warning("Java is not enabled. "
                          "Contact your system administrator.")
            
        def doit(ar):
            ar.info("Going to open url: %s " % url)
            ar.success(open_davlink_url=url)
            # logger.info('20140313 EditTemplate %r', kw)
    
        if filename == local_file:
            doit(ar)
        else:
            def ok(ar2):
                logger.info(
                    "%s made local template copy %s", ar.user, local_file)
                rt.makedirs_if_missing(dirname(local_file))
                shutil.copy(filename, local_file)
                doit(ar2)

            msg = _(
                "Before you can edit this template we must create a "
                "local copy on the server. "
                "This will exclude the template from future updates.")
            ar.info("Gonna copy %s to %s",
                    rt.relpath(filename), rt.relpath(local_file))
            ar.confirm(ok, msg, _("Are you sure?"))
                

# http://10.171.37.173/api/excerpts/ExcerptTypes/5?an=detail


class ClearCacheAction(actions.Action):

    """
    Defines the :guilabel:`Clear cache` button on a Printable record.
    
    The `run_from_ui` method has an optional keyword argmuent
     `force`. This is set to True in `docs/tests/debts.rst`
     to avoid compliations.
    
    """
    sort_index = 51
    url_action_name = 'clear'
    label = _('Clear cache')
    icon_name = 'printer_delete'

    #~ def disabled_for(self,obj,request):
        #~ if not obj.build_time:
            #~ return True

    def get_action_permission(self, ar, obj, state):
        # obj may be None when Lino asks whether this action
        # should be visible in the UI
        if obj is not None and not obj.build_time:
            return False
        return super(ClearCacheAction, self).get_action_permission(ar, obj, state)

    def run_from_ui(self, ar):
        elem = ar.selected_rows[0]

        def doit(ar):
            elem.clear_cache()
            ar.success(_("%s printable cache has been cleared.") %
                       elem, refresh=True)

        t = elem.get_cache_mtime()
        if t is not None and t != elem.build_time:
            logger.info(
                "20140313 %r != %r", elem.get_cache_mtime(), elem.build_time)
            return ar.confirm(
                doit,
                _("This will discard all changes in the generated file."),
                _("Are you sure?"))
        return doit(ar)


class PrintableType(Model):
    "See :class:`dd.PrintableType`."

    templates_group = None
    """
    Default value for `templates_group` is the model's full name.
    """

    class Meta:
        abstract = True

    build_method = BuildMethods.field(
        verbose_name=_("Build method"),
        blank=True, null=True)

    template = models.CharField(_("Template"), max_length=200, blank=True)
    """
    The name of the file to be used as template.
    The list of choices for this field depend on the :attr:`build_method`.
    Ending must correspond to the :attr:`build_method`.
    """

    @classmethod
    def get_template_groups(cls):
        """Note that `get_template_groups` is a **class method** on
        `PrintableType` but an **instance method** on `Printable`.

        """
        #~ return cls.templates_group or cls._meta.app_label
        return [cls.templates_group]  # or full_model_name(cls)

    @chooser(simple_values=True)
    def template_choices(cls, build_method):
        return cls.get_template_choices(
            build_method,
            cls.get_template_groups())

    @classmethod
    def get_template_choices(cls, build_method, template_groups):
        if not build_method:
            build_method = BuildMethods.get_system_default()
        return rt.find_template_config_files(
            build_method.template_ext, *template_groups)


class Printable(object):
    "See :class:`dd.Printable`."

    do_print = DirectPrintAction()
    # Note that :func:`ml.excerpts.set_excerpts_actions` possibly
    # replaces the `do_print` action by a `excerpts.CreateExcerpt`
    # instance.

    edit_template = EditTemplate()

    def before_printable_build(self, bm):
        pass

    def get_template_groups(self):
        return [self.__class__.get_template_group()]

    def filename_root(self):
        return self._meta.app_label + '.' + self.__class__.__name__ \
            + '-' + str(self.pk)

    def get_print_templates(self, bm, action):
        if bm.default_template:
            return [bm.default_template]
        return ['Default' + bm.template_ext]

    def get_default_build_method(self):
        return BuildMethods.get_system_default()

    def get_build_method(self):
        # TypedPrintable  overrides this
        return self.get_default_build_method()


class CachedPrintable(Duplicable, Printable):
    "See :class:`dd.CachedPrintable`."

    do_print = CachedPrintAction()
    do_clear_cache = ClearCacheAction()

    build_time = models.DateTimeField(
        _("build time"), null=True, editable=False)

    build_method = BuildMethods.field()

    class Meta:
        abstract = True

    def full_clean(self, *args, **kwargs):
        if not self.build_method:
            self.build_method = self.get_default_build_method()
        super(CachedPrintable, self).full_clean(*args, **kwargs)

    #~ def print_from_posting(self,posting,ar,**kw):
        #~ return self.do_print.run_from_session(ar,**kw)
    def on_duplicate(self, ar, master):
        super(CachedPrintable, self).on_duplicate(ar, master)
        self.build_time = None
        self.build_method = None

    def get_target_name(self):
        if self.build_time:
            return self.build_method.get_target_name(
                self.do_print, self)

    def get_target_url(self):
        return self.build_method.get_target_url(
            self.do_print, self)

    def get_cache_mtime(self):
        filename = self.get_target_name()
        if not filename:
            return None
        try:
            t = os.path.getmtime(filename)
        except OSError:
            return None
        return datetime.datetime.fromtimestamp(t)

    def clear_cache(self):
        self.build_time = None
        self.save()

    def build_target(elem, ar):
        bm = elem.get_build_method()
        t = bm.build(ar, elem.__class__.do_print, elem)
        if t is None:
            raise Exception("%s : build() returned None?!")
        elem.build_time = datetime.datetime.fromtimestamp(t)
        elem.save()


class TypedPrintable(CachedPrintable):
    "See :class:`dd.TypedPrintable`."

    type = None

    class Meta:
        abstract = True

    def get_printable_type(self):
        return self.type

    def get_template_groups(self):
        ptype = self.get_printable_type()
        if ptype is None:
            return super(TypedPrintable, self).get_template_groups()
        return ptype.get_template_groups()

    def get_default_build_method(self):
        ptype = self.get_printable_type()
        if ptype and ptype.build_method:
            return ptype.build_method
        return super(TypedPrintable, self).get_default_build_method()

    def get_build_method(self):
        if not self.build_method:
            return self.get_default_build_method()
        return self.build_method
        # ptype = self.get_printable_type()
        # if ptype and ptype.build_method:
        #     return ptype.build_method
        # return super(TypedPrintable, self).get_build_method()

    def get_print_templates(self, bm, action):
        ptype = self.get_printable_type()
        if ptype is None:
            return super(TypedPrintable, self).get_print_templates(bm, action)
        tplname = ptype.template or bm.default_template
        if not tplname.endswith(bm.template_ext):
            raise Warning(
                "Invalid template '%s' configured for %s '%s' (expected filename ending with '%s')." %
                (tplname, ptype.__class__.__name__, unicode(ptype), bm.template_ext))
        return [tplname]

