# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
# License: BSD (see file COPYING for details)
"""This module defines the actual :mod:`lino.modlib.weasyprint` build
methods.

"""

from __future__ import unicode_literals
from __future__ import absolute_import
from builtins import str

import logging
logger = logging.getLogger(__name__)

import os
from copy import copy

from django.conf import settings
from django.utils import translation

from lino.modlib.printing.choicelists import DjangoBuildMethod, BuildMethods

try:
    from weasyprint import HTML
except ImportError:
    HTML = None


class WeasyBuildMethod(DjangoBuildMethod):
    """The base class for both build methods.

    """

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
            logger.info(
                "%s render %s -> %s (%r, %s)",
                self.name, tpl, filename, lang, cmd_options)
            context = elem.get_printable_context(ar)
            html = tpl.render(context)
            self.html2file(html, filename)
            return os.path.getmtime(filename)

    def html2file(self, html, filename):
        raise NotImplementedError()


class WeasyPdfBuildMethod(WeasyBuildMethod):
    """Like :class:`WeasyBuildMethod`, but the rendered HTML is then
    passed through weasyprint which converts from HTML to PDF.

    """
    target_ext = '.pdf'
    name = 'weasy2pdf'

    def html2file(self, html, filename):
        pdf = HTML(string=html)
        pdf.write_pdf(filename)


class WeasyHtmlBuildMethod(WeasyBuildMethod):
    """Renders the input template and returns the unmodified output as
    plain HTML.

    """
    target_ext = '.html'
    name = 'weasy2html'

    def html2file(self, html, filename):
        html = html.encode("utf-8")
        file(filename, 'w').write(html)


add = BuildMethods.add_item_instance
add(WeasyHtmlBuildMethod())
add(WeasyPdfBuildMethod())

