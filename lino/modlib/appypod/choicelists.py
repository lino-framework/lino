# -*- coding: UTF-8 -*-
# Copyright 2009-2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""Choicelists for `lino.modlib.appypod`.
"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

import os

from django.conf import settings
from django.utils import translation

from lino.modlib.printing.choicelists import SimpleBuildMethod, BuildMethods

from .appy_renderer import AppyRenderer


class AppyBuildMethod(SimpleBuildMethod):
    """
    Base class for Build Methods that use `.odt` templates designed
    for :term:`appy.pod`.
    
    http://appyframework.org/podRenderingTemplates.html
    """

    template_ext = '.odt'
    templates_name = 'appy'  # subclasses use the same templates directory
    default_template = 'Default.odt'

    def simple_build(self, ar, elem, tpl, target):
        # When the source string contains non-ascii characters, then
        # we must convert it to a unicode string.
        lang = str(elem.get_print_language()
                   or settings.SITE.DEFAULT_LANGUAGE.django_code)
        logger.info(u"appy.pod render %s -> %s (language=%r,params=%s",
                    tpl, target, lang, settings.SITE.appy_params)

        with translation.override(lang):

            context = elem.get_printable_context(ar)
            # 20150721 context.update(ar=ar)

            # backwards compat for existing .odt templates.  Cannot
            # set this earlier because that would cause "render() got
            # multiple values for keyword argument 'self'" exception
            context.update(self=context['this'])

            AppyRenderer(ar, tpl, context, target,
                         **settings.SITE.appy_params).run()
        return os.path.getmtime(target)


class AppyOdtBuildMethod(AppyBuildMethod):
    """
    Generates .odt files from .odt templates.
    
    This method doesn't require OpenOffice nor the
    Python UNO bridge installed
    (except in some cases like updating fields).
    """
    target_ext = '.odt'
    cache_name = 'userdocs'
    #~ cache_name = 'webdav'
    use_webdav = True


class AppyPdfBuildMethod(AppyBuildMethod):
    """
    Generates .pdf files from .odt templates.
    """
    target_ext = '.pdf'


class AppyRtfBuildMethod(AppyBuildMethod):
    """
    Generates .rtf files from .odt templates.
    """
    target_ext = '.rtf'
    cache_name = 'userdocs'
    use_webdav = True


class AppyDocBuildMethod(AppyBuildMethod):
    """
    Generates .doc files from .odt templates.
    """
    target_ext = '.doc'
    cache_name = 'userdocs'
    use_webdav = True


add = BuildMethods.add_item_instance
add(AppyOdtBuildMethod('appyodt'))
add(AppyDocBuildMethod('appydoc'))
add(AppyPdfBuildMethod('appypdf'))
add(AppyRtfBuildMethod('appyrtf'))
