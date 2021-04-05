# -*- coding: UTF-8 -*-
# Copyright 2016-2020 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import os
from copy import copy

try:
    from weasyprint import HTML
except ImportError:
    HTML = None

from django.conf import settings
from django.utils import translation

from lino.api import dd

from lino.modlib.jinja.choicelists import JinjaBuildMethod
from lino.modlib.printing.choicelists import BuildMethods



class WeasyBuildMethod(JinjaBuildMethod):

    template_ext = '.weasy.html'
    templates_name = 'weasy'
    default_template = 'default.weasy.html'


class WeasyHtmlBuildMethod(WeasyBuildMethod):
    target_ext = '.html'
    name = 'weasy2html'

    def html2file(self, html, filename):
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
