# -*- coding: UTF-8 -*-
# Copyright 2016-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from __future__ import unicode_literals
from __future__ import absolute_import
from builtins import str
import six

# import logging
# logger = logging.getLogger(__name__)

import os
from copy import copy

try:
    from weasyprint import HTML
except ImportError:
    HTML = None

from django.conf import settings
from django.utils import translation

from lino.api import dd
from lino.modlib.printing.choicelists import DjangoBuildMethod, BuildMethods


class WeasyBuildMethod(DjangoBuildMethod):

    template_ext = '.weasy.html'
    templates_name = 'weasy'
    default_template = 'default.weasy.html'

    def build(self, ar, action, elem):
        filename = action.before_build(self, elem)
        if filename is None:
            return
        tpl = self.get_template(action, elem)

        lang = str(elem.get_print_language()
                   or settings.SITE.DEFAULT_LANGUAGE.django_code)
        ar = copy(ar)
        ar.renderer = settings.SITE.plugins.jinja.renderer
        # ar.tableattrs = dict()
        # ar.cellattrs = dict(bgcolor="blue")

        with translation.override(lang):
            cmd_options = elem.get_build_options(self)
            dd.logger.info(
                "%s render %s -> %s (%r, %s)",
                self.name, tpl.lino_template_names, filename, lang, cmd_options)
            context = elem.get_printable_context(ar)
            html = tpl.render(context)
            self.html2file(html, filename)
            return os.path.getmtime(filename)

    def html2file(self, html, filename):
        raise NotImplementedError()


class WeasyHtmlBuildMethod(WeasyBuildMethod):
    target_ext = '.html'
    name = 'weasy2html'

    def html2file(self, html, filename):
        if six.PY2:
            html = html.encode("utf-8")
        open(filename, 'w').write(html)


class WeasyPdfBuildMethod(WeasyBuildMethod):
    target_ext = '.pdf'
    name = 'weasy2pdf'

    def html2file(self, html, filename):
        pdf = HTML(string=html)
        pdf.write_pdf(filename)


add = BuildMethods.add_item_instance
add(WeasyHtmlBuildMethod())
add(WeasyPdfBuildMethod())

