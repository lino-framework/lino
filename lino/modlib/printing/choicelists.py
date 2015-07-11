# -*- coding: UTF-8 -*-
# Copyright 2009-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Choicelists for `lino.modlib.printing`.

"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

import os
import cStringIO

from django.conf import settings

from django.template.loader import (select_template, Context,
                                    TemplateDoesNotExist)

from lino.core.choicelists import ChoiceList, Choice
from lino.utils.media import MediaFile
from lino.api import dd, rt, _

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
    default_template = ''  # overridden by lino.modlib.appypod

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

    def __init__(self, name, **kwargs):
        super(BuildMethod, self).__init__(
            name, self.__class__.__name__, name, **kwargs)
        if self.templates_name is None:
            self.templates_name = self.name

    def get_target(self, action, elem):
        "used by `get_target_name`"
        # assert self.name is not None
        return MediaFile(
            self.use_webdav,
            self.cache_name,
            self.value,
            elem.filename_root() + self.target_ext)

    def get_target_name(self, action, elem):
        return self.get_target(action, elem).name

    def get_default_template(self, obj):
        """Theoretically it is possible to write build methods which override
        this.

        """
        if self.default_template:
            return self.default_template
        return 'Default' + self.template_ext
        # return dd.plugins.printing.get_default_template(self, obj)

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
    Usage example see :doc:`/tutorials/pisa/index`.
    """
    # name = 'pisa'
    target_ext = '.pdf'
    template_ext = '.pisa.html'

    def build(self, ar, action, elem):
        import ho.pisa as pisa
        # pisa.showLogging()
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
        if not tpl_leaf.endswith(self.template_ext):
            raise Warning(
                "Invalid template '%s' configured for %s '%s' "
                "(expected filename ending with '%s')." %
                (tpl_leaf, elem.__class__.__name__, unicode(elem),
                 self.template_ext))

        lang = elem.get_print_language() \
            or settings.SITE.DEFAULT_LANGUAGE.django_code
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


class LatexBuildMethod(BuildMethod):

    """
    Generates .pdf files from .tex templates.
    """
    target_ext = '.pdf'
    template_ext = '.tex'

    def simple_build(self, ar, elem, tpl, target):
        # context = dict(instance=elem)
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
    """
    The choicelist of build methods offered on this site.
    """
    verbose_name = _("Build method")
    item_class = BuildMethod
    # app_label = 'lino'
    max_length = 50

    @classmethod
    def get_system_default(cls):
        sc = settings.SITE.site_config
        if sc.default_build_method is not None:
            return sc.default_build_method
        if settings.SITE.default_build_method:
            return cls.get_by_value(
                settings.SITE.default_build_method)
        return cls.appyodt  # hard-coded default


add = BuildMethods.add_item_instance
add(LatexBuildMethod('latex'))
add(PisaBuildMethod('pisa'))
add(RtfBuildMethod('rtf'))
