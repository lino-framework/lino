# -*- coding: UTF-8 -*-
# Copyright 2009-2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Choicelists for `lino.modlib.printing`.

"""

from __future__ import unicode_literals
from future import standard_library
standard_library.install_aliases()
from builtins import str

import logging
logger = logging.getLogger(__name__)

import os
import io

from django.conf import settings


try:
    from django.template import TemplateDoesNotExist
except ImportError:
    from django.template.loader import TemplateDoesNotExist

from django.template.loader import select_template

from lino.core.choicelists import ChoiceList, Choice
from lino.utils.media import MediaFile
from lino.api import rt, _
# from .utils import PrintableObject

try:
    import pyratemp
except ImportError:
    pyratemp = None


class BuildMethod(Choice):
    target_ext = None
    cache_name = 'cache'
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

    def __init__(self, name=None, **kwargs):
        # For build methods, `Choice.name` and `Choice.value` are the
        # same.
        if name is None:
            name = self.name
        super(BuildMethod, self).__init__(
            name, self.__class__.__name__, name, **kwargs)

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

    def get_target_url(self, action, elem):
        return self.get_target(action, elem).url

    def build(self, ar, action, elem):
        raise NotImplementedError


class TemplatedBuildMethod(BuildMethod):

    """Base class for all build methods.  A build method encapsulates the
    process of generating a "printable document" that inserts data
    from the database into a template, using a given combination of a
    template parser and post-processor.

    """
    template_ext = None
    templates_name = None
    default_template = ''  # overridden by lino_xl.lib.appypod

    def __init__(self, *args, **kwargs):
        super(TemplatedBuildMethod, self).__init__(*args, **kwargs)
        if self.templates_name is None:
            self.templates_name = self.name

    def get_default_template(self, obj):
        """Theoretically it is possible to write build methods which override
        this.

        """
        if self.default_template:
            return self.default_template
        return 'Default' + self.template_ext
        # return dd.plugins.printing.get_default_template(self, obj)


class DjangoBuildMethod(TemplatedBuildMethod):

    """
    Using Django's templating engine.
    """

    def get_template(self, action, elem):
        tpls = action.get_print_templates(self, elem)
        if len(tpls) == 0:
            raise Warning("No templates defined for %r" % elem)
        tpls2 = []
        for i in tpls:
            for g in elem.get_template_groups():
                tpls2.append(g+'/'+i)
            # if isinstance(elem, PrintableObject):
            #     for g in elem.get_template_groups():
            #         tpls2.append(g+'/'+i)
            # else:
            #     tpls2.append(elem.get_template_group()+'/'+i)
        #~ logger.debug('make_pisa_html %s',tpls)
        # prefix = '/'.join(elem.get_template_groups())
        # if prefix:
        #     prefix += '/'
        # tpls = [prefix + tpl for tpl in tpls]
        try:
            return select_template(tpls2)
        except TemplateDoesNotExist as e:
            raise Warning("No template found for %s (%s)" % (e, tpls2))
        except Exception as e:
            raise Exception(
                "Error while loading template for %s : %s" % (tpls2, e))

    # ,MEDIA_URL=settings.MEDIA_URL):
    def render_template(self, elem, tpl, **context):
        context.update(
            instance=elem,
            title=str(elem),
            MEDIA_URL=settings.MEDIA_ROOT.replace('\\', '/') + '/',
        )
        return tpl.render(context)


class PisaBuildMethod(DjangoBuildMethod):
    """
    Generates .pdf files from .html templates.
    Requires `pisa <https://pypi.python.org/pypi/pisa>`_.
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

        result = io.BytesIO()
        h = logging.FileHandler(filename + '.log', 'w')
        pisa.log.addHandler(h)
        pdf = pisa.pisaDocument(
            io.BytesIO(html), result, encoding='utf-8')
        pisa.log.removeHandler(h)
        h.close()
        fd = file(filename, 'wb')
        fd.write(result.getvalue())
        fd.close()
        if pdf.err:
            raise Exception("pisa.pisaDocument.err is %r" % pdf.err)
        return os.path.getmtime(filename)


class SimpleBuildMethod(TemplatedBuildMethod):
    """Base for build methods which use Lino's templating system
    (:meth:`find_config_file <lino.core.site.Site.find_config_file>`).

    TODO: check whether this extension to Django's templating system
    is still needed.

    """
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
                (tpl_leaf, elem.__class__.__name__, str(elem),
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
        # if elem is None:
            # return
        target = action.before_build(self, elem)
        if not target:
            return
        tplfile = self.get_template_file(ar, action, elem)
        return self.simple_build(ar, elem, tplfile, target)

    def simple_build(self, ar, elem, tpl, target):
        raise NotImplementedError


class LatexBuildMethod(SimpleBuildMethod):
    """
    Generates `.pdf` files from `.tex` templates.
    Not actively used.
    """
    target_ext = '.pdf'
    template_ext = '.tex'

    def simple_build(self, ar, elem, tpl, target):
        # context = dict(instance=elem)
        raise NotImplementedError


class RtfBuildMethod(SimpleBuildMethod):
    """
    Generates .rtf files from .rtf templates.
    Not actively used.
    """

    target_ext = '.rtf'
    template_ext = '.rtf'
    cache_name = 'userdocs'

    def simple_build(self, ar, elem, tpl, target):
        context = dict(instance=elem)
        t = pyratemp.Template(filename=tpl)
        try:
            result = t(**context)
        except pyratemp.TemplateRenderError as e:
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
        """Return the default build method to be used when really no default
        build method has been defined anywhere, even not in
        :attr:`default_build_method
        <lino.core.site.Site.default_build_method>`.

        """
        sc = settings.SITE.site_config
        if sc.default_build_method:
            return sc.default_build_method
        if settings.SITE.default_build_method:
            return cls.get_by_value(
                settings.SITE.default_build_method)
        return cls.pisa  # hard-coded default


add = BuildMethods.add_item_instance
add(LatexBuildMethod('latex'))
add(PisaBuildMethod('pisa'))
add(RtfBuildMethod('rtf'))
