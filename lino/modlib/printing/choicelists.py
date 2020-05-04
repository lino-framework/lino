# -*- coding: UTF-8 -*-
# Copyright 2009-2017 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""
Choicelists for `lino.modlib.printing`.

"""

import logging ; logger = logging.getLogger(__name__)

import os
import io
from copy import copy

from django.conf import settings
from django.utils import translation


try:
    from django.template import TemplateDoesNotExist
except ImportError:
    from django.template.loader import TemplateDoesNotExist

from django.template.loader import select_template

from lino.core.choicelists import ChoiceList, Choice
from lino.utils.media import MediaFile
from lino.api import rt, _

try:
    import pyratemp
except ImportError:
    pyratemp = None


class BuildMethod(Choice):
    target_ext = None
    cache_name = 'cache'
    use_webdav = False

    def __init__(self, names=None, **kwargs):
        # For build methods, `Choice.names` and `Choice.value` are the
        # same.
        if names is None:
            names = self.name
        super(BuildMethod, self).__init__(
            names, self.__class__.__name__, names, **kwargs)

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

    template_ext = None
    templates_name = None
    default_template = ''  # overridden by lino_xl.lib.appypod

    def __init__(self, *args, **kwargs):
        super(TemplatedBuildMethod, self).__init__(*args, **kwargs)
        if self.templates_name is None:
            assert len(self.names) == 1
            self.templates_name = self.names[0]

    def get_default_template(self, obj):
        """Theoretically it is possible to write build methods which override
        this.

        """
        if self.default_template:
            return self.default_template
        return 'Default' + self.template_ext
        # return dd.plugins.printing.get_default_template(self, obj)


class DjangoBuildMethod(TemplatedBuildMethod):

    def get_template(self, action, elem):
        tpls = action.get_print_templates(self, elem)
        # print('20190506 get_template', tpls)
        if len(tpls) == 0:
            raise Warning("No templates defined for %r" % elem)
        tpls2 = []
        for i in tpls:
            for g in elem.get_template_groups():
                tpls2.append(g+'/'+i)
        # print('20190506 get_template', tpls2)
        # prefix = '/'.join(elem.get_template_groups())
        # if prefix:
        #     prefix += '/'
        # tpls = [prefix + tpl for tpl in tpls]
        try:
            tpl = select_template(tpls2)
            tpl.lino_template_names = tpls2
            return tpl
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
    # name = 'pisa'
    target_ext = '.pdf'
    template_ext = '.pisa.html'

    def build(self, ar, action, elem):
        from xhtml2pdf import pisa
        # pisa.showLogging()
        tpl = self.get_template(action, elem)
        filename = action.before_build(self, elem)
        if filename is None:
            return
        #~ html = self.render_template(elem,tpl,request=ar.request)
        html = self.render_template(elem, tpl, ar=ar)
        html = html.encode("utf-8")
        open(filename + '.html', 'w').write(html)

        result = io.BytesIO()
        h = logging.FileHandler(filename + '.log', 'w')
        pisa.log.addHandler(h)
        pdf = pisa.pisaDocument(
            io.BytesIO(html), result, encoding='utf-8')
        pisa.log.removeHandler(h)
        h.close()
        fd = open(filename, 'wb')
        fd.write(result.getvalue())
        fd.close()
        if pdf.err:
            raise Exception("pisa.pisaDocument.err is %r" % pdf.err)
        return os.path.getmtime(filename)


class SimpleBuildMethod(TemplatedBuildMethod):
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
    target_ext = '.pdf'
    template_ext = '.tex'

    def simple_build(self, ar, elem, tpl, target):
        # context = dict(instance=elem)
        raise NotImplementedError


class RtfBuildMethod(SimpleBuildMethod):
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
        fd = open(target, 'wb')
        fd.write(result)
        fd.close()
        return os.path.getmtime(target)


class XmlBuildMethod(DjangoBuildMethod):
    target_ext = '.xml'
    template_ext = '.xml'
    cache_name = 'xml'

    def build(self, ar, action, elem):
        filename = action.before_build(self, elem)
        if filename is None:
            return
        tpl = self.get_template(action, elem)

        lang = str(elem.get_print_language()
                   or settings.SITE.DEFAULT_LANGUAGE.django_code)

        with translation.override(lang):
            cmd_options = elem.get_build_options(self)
            logger.info(
                "%s render %s -> %s (%r, %s)",
                self.name, tpl, filename, lang, cmd_options)
            ar = copy(ar)
            ar.renderer = settings.SITE.plugins.jinja.renderer
            # ar.tableattrs = dict()
            # ar.cellattrs = dict(bgcolor="blue")
            context = action.get_printable_context(self, elem, ar)
            xml = tpl.render(context)
            self.write2file(xml, filename)

        self.validate_result_file(filename)
        return os.path.getmtime(filename)

    def validate_result_file(self, filename):
        """Validate the generated file.
        """
        pass

    def write2file(self, txt, filename):
        open(filename, 'w').write(txt)



class BuildMethods(ChoiceList):
    # verbose_name = _("Build method")
    verbose_name = _("Print method")
    item_class = BuildMethod
    # app_label = 'lino'
    max_length = 50

    @classmethod
    def get_system_default(cls):
        """Return the default build method to be used.

        Either the one defined in :class:`SiteConfig`, or the one defined by
        :attr:`default_build_method
        <lino.core.site.Site.default_build_method>`.

        """
        sc = settings.SITE.site_config
        if sc.default_build_method:
            return sc.default_build_method
        if settings.SITE.default_build_method:
            bm = cls.get_by_value(
                settings.SITE.default_build_method)
            if bm is None:
                raise Exception("Invalid default_build_method '{}', choices are {}".format(
                    settings.SITE.default_build_method, tuple(cls.get_list_items())))
            return bm
        # return cls.pisa  # hard-coded default


add = BuildMethods.add_item_instance
add(LatexBuildMethod('latex'))
# add(PisaBuildMethod('pisa'))
add(RtfBuildMethod('rtf'))
add(XmlBuildMethod('xml'))
