# -*- coding: UTF-8 -*-
# Copyright 2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)


import os
from copy import copy

from django.conf import settings
from django.utils import translation

from lino.api import dd

from lino.modlib.jinja.choicelists import JinjaBuildMethod
from lino.modlib.printing.choicelists import BuildMethods

class PublisherBuildMethod(JinjaBuildMethod):

    template_ext = '.pub.html'
    templates_name = 'pub'
    default_template = 'default.pub.html'
    target_ext = '.html'
    name = 'pub'

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


BuildMethods.add_item_instance(PublisherBuildMethod())
