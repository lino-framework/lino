# -*- coding: UTF-8 -*-
# Copyright 2020 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)


import os
from copy import copy

from django.db import models
from django.conf import settings
from django.utils import translation

from lino.api import dd, _
from lino.mixins.registrable import RegistrableState

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



class PublishableState(RegistrableState):
    is_published = False


class PublishableStates(dd.Workflow):
    item_class = PublishableState
    verbose_name = _("Publishable state")
    verbose_name_plural = _("Publishable states")
    column_names = "value name text is_published"

    @classmethod
    def get_published_states(cls):
        return [o for o in cls.objects() if o.is_published]

    @dd.virtualfield(models.BooleanField(_("published")))
    def is_published(cls, choice, ar):
        return choice.is_published

add = PublishableStates.add_item
add('10', _("Draft"), 'draft')
add('20', _("Published"), 'published', is_published=True)
add('30', _("Removed"), 'removed')
