# -*- coding: UTF-8 -*-
# Copyright 2013-2014 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""
"""
from builtins import str
from builtins import object

import logging
logger = logging.getLogger(__name__)

import os

from django.utils import translation

from lino.sphinxcontrib.actordoc import Lino2rstDirective

from lino.core import actors


class ScreenshotDirective(Lino2rstDirective):

    def get_rst(self):
        assert len(self.content) == 0
        assert len(self.arguments) == 1
        ss = SCREENSHOTS[self.arguments[0]]
        return "\n\n.. image:: %s\n\n" % ss.get_filename(translation.get_language())


def get_screenshots(language):
    #~ print 20130515, profiles2user.values()
    #~ print 20130515, actors.actors_list
    for actor in actors.actors_list:
            for ar in actor.get_screenshot_requests(language):
                yield Screenshot(ar)


class Screenshot(object):
    #~ def __init__(self,name,url,username=None):

    def __init__(self, ar):
        if ar.bound_action is not ar.actor.default_action:
            name = ar.bound_action.full_name()
        else:
            name = str(ar.actor)
        self.name = name
        #~ self.url = url
        #~ self.username = username
        self.ar = ar
        self.language = ar.get_user().language

    def get_filename(self, root):
        return os.path.join(root, self.language, '%s.jpg' % self.name)

    def get_url(self, urlbase, *args, **kw):
        #~ kw[constants.URL_PARAM_USER_LANGUAGE] = self.language
        if self.ar.bound_action.action.action_name == 'detail':
            if len(args) == 0:
                try:
                    args = [str(iter(self.ar).next().pk)]
                except StopIteration:
                    return None
        return urlbase + self.ar.get_request_url(*args, **kw)
        #~ return '%s%s?ul=%s' % (root,url,self.language.django_code)

#~ def register_screenshot(*args,**kw):
    #~ ss = Screenshot(*args,**kw)
    #~ SCREENSHOTS[ss.name] = ss
    #~ return ss


def setup(app):
    app.add_directive('screenshot', ScreenshotDirective)
