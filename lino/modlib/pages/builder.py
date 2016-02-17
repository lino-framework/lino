# -*- coding: UTF-8 -*-
# Copyright 2012-2013 Luc Saffre
# License: BSD (see file COPYING for details)

import logging
logger = logging.getLogger(__name__)

#~ import datetime
from django.conf import settings
#~ from lino.utils.instantiator import Instantiator

from lino.api import dd, rt
from lino.utils import AttrDict
from lino.utils.restify import restify
from lino.utils.restify import doc2rst

#~ PAGES = {}


def babelfield(name, language):
    if language == settings.SITE.DEFAULT_LANGUAGE.django_code:
        return name
    return name + '_' + language


def page(ref, language, title, body, parent=None, raw_html=False):
    if not settings.SITE.get_language_info(language):
        return
    pages = dd.resolve_app('pages', strict=True)
    obj = pages.lookup(ref, None)
    #~ obj = PAGES.get(ref)
    if parent is not None:
        parent = pages.lookup(parent)
    if obj is None:
        #~ kw = dict(,parent=parent)
        obj = pages.create_page(ref=ref)
        #~ PAGES[ref] = obj
        #~ if not ref:
            #~ logger.info("20130109 define index page %r --> %r",language,body)
    #~ else:
        #~ if not ref:
            #~ logger.info("20130109 override index page %r --> %r",language,body)

    setattr(obj, 'raw_html', raw_html)
    setattr(obj, 'parent', parent)
    setattr(obj, babelfield('title', language), title)
    setattr(obj, babelfield('body', language), body.strip())
    # must save it already here so that subsequent pages of the same fixture
    # can use it as parent.
    obj.full_clean()
    obj.save()
    #~ obj.update(babelfield('body',**{language:body}))
    #~ logger.info("20121227 builder.page(%r,%r,%r) -> %s",ref,language,title,obj.keys())
    #~ obj.title.texts[language] = title
    #~ obj.body.texts[language] = body


def objects():
    yield settings.SITE.site_config
    if False:
        global PAGES
        #~ print 20121227, __file__, [obj['ref'] for obj in PAGES.values()]
        rv = []
        for obj in list(PAGES.values()):
            yield obj
            #~ rv.append()

        PAGES = {}
        #~ return rv
