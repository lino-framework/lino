# -*- coding: UTF-8 -*-
# Copyright 2016 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
"""Choicelists for `lino.modlib.wkhtmltopdf`.
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


try:
    from wkhtmltopdf.utils import render_pdf_from_template
except ImportError:
    render_pdf_from_template = None


class WkBuildMethod(DjangoBuildMethod):
    """
    """

    template_ext = '.wk.html'
    templates_name = 'wk'
    default_template = 'default.wk.html'
    target_ext = '.pdf'
    # cache_name = 'wkhtmltopdf'

    def build(self, ar, action, elem):
        if render_pdf_from_template is None:
            raise Warning(
                "wkhtmltopdf build fails because django-wkhtmltopdf "
                "is not installed.")
        filename = action.before_build(self, elem)
        if filename is None:
            return
        tpl = self.get_template(action, elem)
        htpl = None
        ftpl = None

        lang = str(elem.get_print_language()
                   or settings.SITE.DEFAULT_LANGUAGE.django_code)
        with translation.override(lang):
            cmd_options = elem.get_build_options(self)
            logger.info(
                "wkhtmltopdf render %s -> %s (%r, %s)",
                tpl, filename, lang, cmd_options)

            context = elem.get_printable_context(ar)
            html = render_pdf_from_template(
                tpl, htpl, ftpl, context, cmd_options)
            # html = html.encode("utf-8")
            file(filename, 'w').write(html)
            return os.path.getmtime(filename)

add = BuildMethods.add_item_instance
add(WkBuildMethod('wkhtmltopdf'))

