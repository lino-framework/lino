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

from wkhtmltopdf.utils import render_to_temporary_file


class WeasyBuildMethod(DjangoBuildMethod):
    """
    """

    template_ext = '.weasy.html'
    templates_name = 'weasy'
    default_template = 'default.weasy.html'
    target_ext = '.pdf'

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
                "weasyprint render %s -> %s (%r, %s)",
                tpl, filename, lang, cmd_options)

            context = elem.get_printable_context(ar)
            # html = render_to_temporary_file(tpl, context)
            html = tpl.render(context)
            pdf = HTML(string=html)
            pdf.write_pdf(filename)
            # html = render_pdf_from_template(
            #     tpl, htpl, ftpl, context, cmd_options)
            # html = html.encode("utf-8")
            # file(filename, 'w').write(html)
            return os.path.getmtime(filename)

add = BuildMethods.add_item_instance
add(WeasyBuildMethod('weasy'))

