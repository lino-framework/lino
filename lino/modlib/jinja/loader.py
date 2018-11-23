# Copyright 2012-2015 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""Defines a Loader which is automatically installed to
`TEMPLATE_LOADERS` by :mod:`lino.core.site`

"""

from __future__ import unicode_literals
from __future__ import print_function
from builtins import object

import logging
logger = logging.getLogger(__name__)

from jinja2.exceptions import TemplateNotFound


from django.conf import settings
# from django.utils.translation import ugettext_lazy as _
from django.template.loaders.base import Loader as BaseLoader

from django.template import TemplateDoesNotExist

from lino.core import requests


class DjangoJinjaTemplate(object):

    """
    used e.g. to render :srcref:`/lino/lino/config/500.html`
    """

    def __init__(self, jt):
        self.jt = jt

    def render(self, context):
        # flatten the Django Context into a single dictionary.
        #~ logger.info("20130118 %s",context)
        context_dict = {}
        for d in context.dicts:
            context_dict.update(d)
        # extend_context(context_dict)
        ar = requests.BaseRequest(
            renderer=settings.SITE.plugins.jinja.renderer)
            # renderer=settings.SITE.kernel.default_renderer)
        context_dict = ar.get_printable_context(**context_dict)
        context_dict.setdefault('request', None)
        #context_dict.setdefault('ar', ar)
        #~ logger.info("20130118 %s",context_dict.keys())
        return self.jt.render(context_dict)


class Loader(BaseLoader):

    is_usable = True

    def load_template(self, template_name, template_dirs=None):
        #~ source, origin = self.load_template_source(template_name, template_dirs)
        env = settings.SITE.plugins.jinja.renderer.jinja_env

        try:
            jt = env.get_template(template_name)
        except TemplateNotFound:
            raise TemplateDoesNotExist(template_name)
        template = DjangoJinjaTemplate(jt)
        return template, None

