# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
# License: BSD (see file COPYING for details)
"""Choicelists for `lino.modlib.weasyprint`.
"""

from __future__ import unicode_literals
from __future__ import absolute_import
from builtins import str

import logging
logger = logging.getLogger(__name__)

import os

from django.conf import settings
from django.utils import translation

from lino.modlib.printing.choicelists import DjangoBuildMethod, BuildMethods

from weasyprint import HTML


class WeasyBuildMethod(DjangoBuildMethod):
    """
    """

    template_ext = '.weasy.html'
    templates_name = 'weasy'
    default_template = 'default.weasy.html'
    target_ext = '.html'

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

            context = elem.get_printable_context(ar)
            html = tpl.render(context)
            self.html2file(html, filename)
            return os.path.getmtime(filename)

    def html2file(self, html, filename):
        html = html.encode("utf-8")
        file(filename, 'w').write(html)


class WeasyPdfBuildMethod(WeasyBuildMethod):

    target_ext = '.pdf'

    def html2file(self, html, filename):
        pdf = HTML(string=html)
        pdf.write_pdf(filename)


add = BuildMethods.add_item_instance
add(WeasyBuildMethod('weasy2html'))
add(WeasyPdfBuildMethod('weasy2pdf'))

